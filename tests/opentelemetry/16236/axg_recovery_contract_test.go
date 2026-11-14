// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Internal, independent AETHER X GLOBAL fault-injection qualification for upstream
// https://github.com/open-telemetry/opentelemetry-collector/issues/16236
//
// Copy ONLY into an isolated exact-HEAD upstream checkout under
// exporter/exporterhelper/internal/queue/axg_recovery_contract_test.go.
// This is a proposed regression TEST, not a patch or upstream contribution.

package queue

import (
	"context"
	"fmt"
	"sort"
	"strconv"
	"testing"

	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/collector/extension/xextension/storage"
)

// axgRecoveryCut simulates process death immediately after the storage transaction
// that retires an in-flight payload has COMMITTED. It does not kill an actual process.
type axgRecoveryCut struct{}

// axgCommittedStore makes Batch a single atomic in-memory commit. Only fixture
// operations use this isolated client: no actual file_storage or production data.
type axgCommittedStore struct {
	records    map[string][]byte
	armed      bool
	cutReached bool
}

func newAXGCommittedStore() *axgCommittedStore {
	return &axgCommittedStore{records: make(map[string][]byte)}
}

func (s *axgCommittedStore) Get(ctx context.Context, key string) ([]byte, error) {
	op := storage.GetOperation(key)
	if err := s.Batch(ctx, op); err != nil {
		return nil, err
	}
	return op.Value, nil
}

func (s *axgCommittedStore) Set(ctx context.Context, key string, value []byte) error {
	return s.Batch(ctx, storage.SetOperation(key, value))
}

func (s *axgCommittedStore) Delete(ctx context.Context, key string) error {
	return s.Batch(ctx, storage.DeleteOperation(key))
}

func (s *axgCommittedStore) Close(context.Context) error { return nil }

func (s *axgCommittedStore) Batch(_ context.Context, ops ...*storage.Operation) error {
	// No partial commits: staged writes are published together.
	updated := make(map[string][]byte, len(s.records))
	for k, v := range s.records {
		updated[k] = append([]byte(nil), v...)
	}

	deletesInFlight := false
	for _, op := range ops {
		switch op.Type {
		case storage.Get:
			op.Value = append([]byte(nil), updated[op.Key]...)
		case storage.Set:
			updated[op.Key] = append([]byte(nil), op.Value...)
		case storage.Delete:
			if s.armed && (op.Key == "0" || op.Key == "1") {
				deletesInFlight = true
			}
			delete(updated, op.Key)
		default:
			return fmt.Errorf("unsupported storage operation %d", op.Type)
		}
	}

	s.records = updated
	if deletesInFlight {
		s.armed = false
		s.cutReached = true
		panic(axgRecoveryCut{})
	}
	return nil
}

func axgCreateInflightFixture(t *testing.T, store *axgCommittedStore) {
	t.Helper()
	ctx := context.Background()
	pq := createTestPersistentQueueWithClient(store)
	for _, val := range []intRequest{11, 22, 33} {
		require.NoError(t, pq.Offer(ctx, val))
	}
	// Keep two requests in-flight. Their completion callbacks are deliberately
	// not invoked, modeling a consumer process that did not acknowledge them.
	for _, expected := range []intRequest{11, 22} {
		_, got, _, ok := pq.Read(ctx)
		require.True(t, ok)
		require.Equal(t, expected, got)
	}
	require.Equal(t, []uint64{0, 1}, pq.metadata.CurrentlyDispatchedItems)
}

func axgDurableInventory(t *testing.T, pq *persistentQueue[intRequest]) []intRequest {
	t.Helper()
	ctx := context.Background()
	found := make([]intRequest, 0)
	for i := pq.metadata.ReadIndex; i < pq.metadata.WriteIndex; i++ {
		raw, err := pq.client.Get(ctx, strconv.FormatUint(i, 10))
		require.NoError(t, err)
		if len(raw) == 0 {
			continue
		}
		_, val, err := (int64Encoding{}).Unmarshal(raw)
		require.NoError(t, err)
		found = append(found, val)
	}
	sort.Slice(found, func(i, j int) bool { return found[i] < found[j] })
	return found
}

func TestAXGRecoveryUninterruptedControl(t *testing.T) {
	store := newAXGCommittedStore()
	axgCreateInflightFixture(t, store)
	restarted := createTestPersistentQueueWithClient(store)
	found := axgDurableInventory(t, restarted)
	require.Equal(t, []intRequest{11, 22, 33}, found,
		"ordinary restart should not lose acknowledged-inflight or queued data")
	t.Logf("AXG_CONTROL_OK observed_ids=%v", found)
}

func TestAXGRecoveryCutAfterCommittedRetirement(t *testing.T) {
	store := newAXGCommittedStore()
	axgCreateInflightFixture(t, store)

	store.armed = true
	var recovered any
	func() {
		defer func() { recovered = recover() }()
		_ = createTestPersistentQueueWithClient(store)
	}()
	if _, ok := recovered.(axgRecoveryCut); !ok {
		t.Fatalf("AXG_CUT_NOT_REACHED: expected simulated committed retirement cut, got %#v", recovered)
	}
	require.True(t, store.cutReached)

	restarted := createTestPersistentQueueWithClient(store)
	found := axgDurableInventory(t, restarted)
	expected := []intRequest{11, 22, 33}
	if !equalAXGRequests(found, expected) {
		t.Fatalf("AXG_LOSS_CONFIRMED after committed retirement and restart: want=%v got=%v", expected, found)
	}
	t.Logf("AXG_CRASH_RECOVERY_SAFE ids=%v", found)
}

func equalAXGRequests(a, b []intRequest) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

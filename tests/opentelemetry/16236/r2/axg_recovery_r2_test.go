// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

package queue

import (
	"context"
	"encoding/binary"
	"fmt"
	"testing"

	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/collector/extension/xextension/storage"
	"go.opentelemetry.io/collector/exporter/exporterhelper/internal/request"
)

func axgLegacyFixture(t *testing.T, store *axgCommittedStore) {
	t.Helper()
	ctx := context.Background()
	require.NoError(t, store.Set(ctx, legacyReadIndexKey, binary.LittleEndian.AppendUint64(nil, 2)))
	require.NoError(t, store.Set(ctx, legacyWriteIndexKey, binary.LittleEndian.AppendUint64(nil, 3)))
	require.NoError(t, store.Set(ctx, legacyCurrentlyDispatchedItemsKey, itemIndexArrayToBytes([]uint64{0, 1})))
	for i, raw := range []string{"11", "22", "33"} {
		require.NoError(t, store.Set(ctx, getItemKey(uint64(i)), []byte(raw)))
	}
}

func axgExpectRestartSurvivors(t *testing.T, store *axgCommittedStore) {
	t.Helper()
	restarted := createTestPersistentQueueWithClient(store)
	require.Equal(t, []intRequest{11, 22, 33}, axgDurableInventory(t, restarted))
}

// A transactionally committed first move must leave a replayable second move.
func TestAXGRecoveryTwoInterruptedCommits(t *testing.T) {
	store := newAXGCommittedStore()
	axgCreateInflightFixture(t, store)
	for cut := 1; cut <= 2; cut++ {
		store.armed = true
		var panicValue any
		func() {
			defer func() { panicValue = recover() }()
			_ = createTestPersistentQueueWithClient(store)
		}()
		_, ok := panicValue.(axgRecoveryCut)
		require.Truef(t, ok, "cut %d not reached, panic=%#v", cut, panicValue)
		t.Logf("AXG_CUT_%d_COMMITTED", cut)
	}
	axgExpectRestartSurvivors(t, store)
	t.Log("AXG_REPEATED_CRASH_SAFE")
}

// A qmv0 commit during a legacy upgrade must preserve remaining in-flight IDs.
func TestAXGRecoveryLegacyCommittedCut(t *testing.T) {
	store := newAXGCommittedStore()
	axgLegacyFixture(t, store)
	store.armed = true
	var panicValue any
	func() {
		defer func() { panicValue = recover() }()
		_ = createTestPersistentQueueWithClient(store)
	}()
	_, ok := panicValue.(axgRecoveryCut)
	require.True(t, ok, "legacy cut not reached")
	axgExpectRestartSurvivors(t, store)
	t.Log("AXG_LEGACY_CRASH_SAFE")
}

type axgRejectFirstMoveStore struct {
	*axgCommittedStore
	reject bool
}

func (s *axgRejectFirstMoveStore) Batch(ctx context.Context, ops ...*storage.Operation) error {
	if s.reject {
		for _, op := range ops {
			if op.Type == storage.Delete && (op.Key == "0" || op.Key == "1") {
				s.reject = false
				return fmt.Errorf("AXG_INJECTED_COMMIT_REJECTION")
			}
		}
	}
	return s.axgCommittedStore.Batch(ctx, ops...)
}

// On a non-committed storage error, recovery should fail closed; no old payload
// must be retired or accepted as recovered when its Batch did not commit.
func TestAXGRecoveryRejectsUncommittedBatchFailure(t *testing.T) {
	base := newAXGCommittedStore()
	axgCreateInflightFixture(t, base)
	store := &axgRejectFirstMoveStore{axgCommittedStore: base, reject: true}
	pq := newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 1000)).(*persistentQueue[intRequest])
	err := pq.initClient(context.Background(), store)
	require.ErrorContains(t, err, "AXG_INJECTED_COMMIT_REJECTION")
	require.Equal(t, []intRequest{11, 22, 33}, axgDurableInventory(t, createTestPersistentQueueWithClient(base)))
	t.Log("AXG_ERROR_FAIL_CLOSED")
}

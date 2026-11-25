// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Independent adversarial tests for the internal OTel #16236 experimental
// candidate, on real on-disk bbolt. No upstream/production distribution used.
package queue

import (
	"context"
	"errors"
	"fmt"
	"path/filepath"
	"sort"
	"strconv"
	"testing"

	"github.com/stretchr/testify/require"
	"go.etcd.io/bbolt"
	"go.opentelemetry.io/collector/exporter/exporterhelper/internal/request"
	"go.opentelemetry.io/collector/extension/xextension/storage"
)

func axgIndependentPhysicalInventory(t *testing.T, c *axgBoltClient) []intRequest {
	t.Helper()
	var actual []intRequest
	err := c.db.View(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket(axgBoltBucket)
		if bucket == nil {
			return errors.New("missing default bucket")
		}
		return bucket.ForEach(func(key, value []byte) error {
			if _, err := strconv.ParseUint(string(key), 10, 64); err != nil {
				return nil
			}
			_, item, err := (int64Encoding{}).Unmarshal(value)
			if err != nil {
				return fmt.Errorf("physical item key=%q: %w", key, err)
			}
			actual = append(actual, item)
			return nil
		})
	})
	require.NoError(t, err)
	sort.Slice(actual, func(i, j int) bool { return actual[i] < actual[j] })
	return actual
}

func TestAXGIndependentNativeRepeatRestartAndPhysicalUniqueness(t *testing.T) {
	for _, legacy := range []bool{false, true} {
		t.Run(fmt.Sprintf("legacy_%v", legacy), func(t *testing.T) {
			path := filepath.Join(t.TempDir(), "durable.db")
			initial := axgOpenBolt(t, path, 0)
			axgSeedNative(t, initial, legacy)
			require.NoError(t, initial.Close(context.Background()))
			for n := 1; n <= 4; n++ {
				client := axgOpenBolt(t, path, 0)
				queue := createTestPersistentQueueWithClient(client)
				got := axgDurableInventory(t, queue)
				require.Equal(t, []intRequest{11, 22, 33}, got)
				require.Empty(t, queue.metadata.CurrentlyDispatchedItems)
				physical := axgIndependentPhysicalInventory(t, client)
				require.Equal(t, []intRequest{11, 22, 33}, physical,
					"no deleted in-flight original key may survive as a second physical copy")
				t.Logf("AXG_INDEPENDENT_RESTART_OK legacy=%v iteration=%d logical=%v physical=%v", legacy, n, got, physical)
				require.NoError(t, client.Close(context.Background()))
			}
		})
	}
}

type axgIndependentRejectMove struct{ storage.Client }

func (c axgIndependentRejectMove) Batch(ctx context.Context, ops ...*storage.Operation) error {
	for _, op := range ops {
		if op.Type == storage.Delete && (op.Key == "0" || op.Key == "1") {
			return fmt.Errorf("injected pre-commit full disk during in-flight move: %w", storage.ErrStorageFull)
		}
	}
	return c.Client.Batch(ctx, ops...)
}

func TestAXGIndependentPreCommitWriteFailurePreservesDurableItems(t *testing.T) {
	path := filepath.Join(t.TempDir(), "rejected-move.db")
	initial := axgOpenBolt(t, path, 0)
	axgSeedNative(t, initial, false)
	require.NoError(t, initial.Close(context.Background()))
	client := axgOpenBolt(t, path, 0)
	failing := axgIndependentRejectMove{Client: client}
	queue := newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 1000)).(*persistentQueue[intRequest])
	err := queue.initClient(context.Background(), failing)
	require.Error(t, err, "ambiguous or failed recovery must abort initialization")
	require.ErrorContains(t, err, "injected pre-commit full disk")
	t.Logf("AXG_INDEPENDENT_FAILED_MOVE_REJECTED error=%v", err)
	require.NoError(t, client.Close(context.Background()))
	reopened := axgOpenBolt(t, path, 0)
	recovered := createTestPersistentQueueWithClient(reopened)
	require.Equal(t, []intRequest{11, 22, 33}, axgDurableInventory(t, recovered))
	require.Equal(t, []intRequest{11, 22, 33}, axgIndependentPhysicalInventory(t, reopened))
	require.NoError(t, reopened.Close(context.Background()))
	t.Log("AXG_INDEPENDENT_PRECOMMIT_ROLLBACK_OK: injected error, no missing/duplicate physical items")
}

// A characterization test, NOT a claim that corrupt metadata is safe.
// The historical upstream queue explicitly resets metadata on decode errors.
// This test preserves adverse evidence while separating inherited semantics
// from the narrower committed-bbolt-copy crash recovery claim.
func TestAXGIndependentCorruptedMetadataCharacterization(t *testing.T) {
	path := filepath.Join(t.TempDir(), "corrupt-meta.db")
	client := axgOpenBolt(t, path, 0)
	queue := createTestPersistentQueueWithClient(client)
	require.NoError(t, queue.Offer(context.Background(), intRequest(11)))
	require.NoError(t, queue.Offer(context.Background(), intRequest(22)))
	require.Equal(t, []intRequest{11, 22}, axgIndependentPhysicalInventory(t, client))
	require.NoError(t, client.Set(context.Background(), metadataKey, []byte{0xff, 0xff, 0xff}))
	require.NoError(t, client.Close(context.Background()))
	reopened := axgOpenBolt(t, path, 0)
	restarted := newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 1000)).(*persistentQueue[intRequest])
	err := restarted.initClient(context.Background(), reopened)
	physical := axgIndependentPhysicalInventory(t, reopened)
	require.Equal(t, []intRequest{11, 22}, physical, "corrupt metadata must not physically erase the payload during this test")
	if err == nil && restarted.metadata.WriteIndex == 0 {
		t.Log("AXG_INDEPENDENT_ADVERSE_FINDING: corrupt qmv0 silently reset read/write indices while physical IDs 11,22 remain; data logically inaccessible until manual recovery")
	} else {
		t.Logf("AXG_INDEPENDENT_METADATA_CORRUPTION_OUTCOME err=%v read=%d write=%d", err, restarted.metadata.ReadIndex, restarted.metadata.WriteIndex)
	}
	require.NoError(t, reopened.Close(context.Background()))
}

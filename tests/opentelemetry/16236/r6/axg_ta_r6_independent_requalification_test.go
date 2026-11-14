// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Independent AETHER TEST ARCHITECT R6 adversarial regressions.
// This file is intentionally not a modification of the engineering R6 tests.
package queue

import (
    "bytes"
    "context"
    "fmt"
    "path/filepath"
    "sort"
    "strconv"
    "testing"

    "github.com/stretchr/testify/require"
    "go.opentelemetry.io/collector/extension/xextension/storage"
)

func axgTAR6PhysicalInventory(t *testing.T, c storage.Client) []intRequest {
    t.Helper()
    walker, ok := c.(storage.Walker)
    require.True(t, ok, "actual Contrib file_storage must expose a Walker")
    got := []intRequest{}
    err := walker.Walk(context.Background(), func(key string, raw []byte) ([]*storage.Operation, error) {
        if _, err := strconv.ParseUint(key, 10, 64); err != nil {
            return nil, nil
        }
        _, val, err := (int64Encoding{}).Unmarshal(raw)
        if err != nil {
            return nil, fmt.Errorf("cannot decode physical request key %q: %w", key, err)
        }
        got = append(got, val)
        return nil, nil
    })
    require.NoError(t, err)
    sort.Slice(got, func(i, j int) bool { return got[i] < got[j] })
    return got
}

func TestAXGTAR6CleanNewQueueControl(t *testing.T) {
    dir := filepath.Join(t.TempDir(), "new")
    ext, client := axgR5OpenFileStorage(t, dir)
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(context.Background(), client))
    require.Equal(t, int64(0), q.Size())
    require.Empty(t, axgTAR6PhysicalInventory(t, client))
    axgR5CloseFileStorage(t, ext, client)
    ext, client = axgR5OpenFileStorage(t, dir)
    q = axgR5NewQueue()
    require.NoError(t, q.initClient(context.Background(), client))
    require.Equal(t, int64(0), q.Size())
    require.Empty(t, axgTAR6PhysicalInventory(t, client))
    axgR5CloseFileStorage(t, ext, client)
    t.Log("AXG_TA_R6_CLEAN_CONTROL_PASS")
}

func TestAXGTAR6RepeatedRealContribReopen(t *testing.T) {
    for _, legacy := range []bool{false, true} {
        t.Run(fmt.Sprintf("legacy_%t", legacy), func(t *testing.T) {
            dir := filepath.Join(t.TempDir(), "real-filestorage")
            ext, client := axgR5OpenFileStorage(t, dir)
            ctx := context.Background()
            if legacy {
                require.NoError(t, client.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(2)))
                require.NoError(t, client.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(3)))
                require.NoError(t, client.Set(ctx, legacyCurrentlyDispatchedItemsKey, itemIndexArrayToBytes([]uint64{0, 1})))
                for i, val := range []int{11, 22, 33} {
                    require.NoError(t, client.Set(ctx, strconv.Itoa(i), []byte(strconv.Itoa(val))))
                }
            } else {
                q := axgR5NewQueue()
                require.NoError(t, q.initClient(ctx, client))
                for _, val := range []intRequest{11, 22, 33} {
                    require.NoError(t, q.Offer(ctx, val))
                }
                for _, want := range []intRequest{11, 22} {
                    _, got, _, ok := q.Read(ctx)
                    require.True(t, ok)
                    require.Equal(t, want, got)
                }
            }
            axgR5CloseFileStorage(t, ext, client)
            for n := 1; n <= 5; n++ {
                ext, client = axgR5OpenFileStorage(t, dir)
                q := axgR5NewQueue()
                require.NoError(t, q.initClient(ctx, client))
                require.Equal(t, int64(3), q.Size(), "capacity/inventory changed at fresh reopen")
                require.Empty(t, q.metadata.CurrentlyDispatchedItems, "phantom in-flight state")
                require.Equal(t, []intRequest{11, 22, 33}, axgTAR6PhysicalInventory(t, client), "missing or duplicate persisted numeric payload")
                axgR5CloseFileStorage(t, ext, client)
                t.Logf("AXG_TA_R6_REOPEN_PASS legacy=%t cycle=%d", legacy, n)
            }
        })
    }
}

func TestAXGTAR6CorruptLegacyMustFailClosedWithoutOrphaning(t *testing.T) {
    // This intentionally challenges a DIFFERENT legacy error boundary from
    // the previously known qmv0-corruption failures. No recovery writes should
    // occur when an existing legacy read index cannot be decoded.
    ctx := context.Background()
    dir := filepath.Join(t.TempDir(), "corrupt-legacy-ri")
    ext, client := axgR5OpenFileStorage(t, dir)
    invalidRI := []byte{0x01, 0x02}
    require.NoError(t, client.Set(ctx, legacyReadIndexKey, invalidRI))
    require.NoError(t, client.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
    require.NoError(t, client.Set(ctx, getItemKey(0), []byte("11")))
    axgR5CloseFileStorage(t, ext, client)

    ext, client = axgR5OpenFileStorage(t, dir)
    q := axgR5NewQueue()
    initErr := q.initClient(ctx, client)
    originalRI, riErr := client.Get(ctx, legacyReadIndexKey)
    require.NoError(t, riErr)
    qmv0, metaErr := client.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    physical := axgTAR6PhysicalInventory(t, client)
    axgR5CloseFileStorage(t, ext, client)
    if initErr == nil {
        t.Error("AXG_TA_R6_LEGACY_RESET_DEFECT: corrupt existing legacy read index was silently accepted")
    }
    if !bytes.Equal(invalidRI, originalRI) {
        t.Errorf("AXG_TA_R6_LEGACY_RESET_DEFECT: legacy read index overwritten/deleted: %x", originalRI)
    }
    if len(qmv0) != 0 {
        t.Errorf("AXG_TA_R6_LEGACY_RESET_DEFECT: new consolidated metadata was written after invalid legacy input: %x", qmv0)
    }
    require.Equal(t, []intRequest{11}, physical, "original durable request must remain physically present")
    t.Logf("AXG_TA_R6_LEGACY_OBSERVED init_error=%v physical=%v", initErr, physical)
}

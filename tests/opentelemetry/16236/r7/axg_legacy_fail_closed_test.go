// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// R7 regression contracts are additive: preserve upstream and independently
// authored R6 tests unchanged, and use actual Contrib file_storage throughout.
package queue

import (
    "bytes"
    "context"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
)

func TestAXGR7LegacyMetadataMustFailClosed(t *testing.T) {
    for _, tc := range []struct {
        name string
        ri, wi []byte
    }{
        {"invalid_read_index", []byte{0x01, 0x02}, bytesForAXGIndex(1)},
        {"invalid_write_index", bytesForAXGIndex(0), []byte{0x03, 0x04}},
        {"missing_read_index", nil, bytesForAXGIndex(1)},
        {"missing_write_index", bytesForAXGIndex(0), nil},
        {"read_after_write", bytesForAXGIndex(2), bytesForAXGIndex(1)},
        {"trailing_bytes_in_read_index", append(bytesForAXGIndex(0), byte(0xff)), bytesForAXGIndex(1)},
    } {
        t.Run(tc.name, func(t *testing.T) {
            ctx := context.Background()
            dir := filepath.Join(t.TempDir(), "legacy")
            require.NoError(t, os.MkdirAll(dir, 0o700))
            ext, client := axgR5OpenFileStorage(t, dir)
            if tc.ri != nil {
                require.NoError(t, client.Set(ctx, legacyReadIndexKey, tc.ri))
            }
            if tc.wi != nil {
                require.NoError(t, client.Set(ctx, legacyWriteIndexKey, tc.wi))
            }
            require.NoError(t, client.Set(ctx, getItemKey(0), []byte("11")))
            axgR5CloseFileStorage(t, ext, client)

            ext, client = axgR5OpenFileStorage(t, dir)
            q := axgR5NewQueue()
            err := q.initClient(ctx, client)
            require.ErrorContains(t, err, "legacy", "unsafe startup should refuse malformed or incomplete legacy metadata")
            gotRI, riErr := client.Get(ctx, legacyReadIndexKey)
            gotWI, wiErr := client.Get(ctx, legacyWriteIndexKey)
            gotQmv0, qErr := client.Get(ctx, metadataKey)
            require.NoError(t, riErr)
            require.NoError(t, wiErr)
            require.NoError(t, qErr)
            require.True(t, bytes.Equal(tc.ri, gotRI), "legacy ri must not be changed")
            require.True(t, bytes.Equal(tc.wi, gotWI), "legacy wi must not be changed")
            require.Empty(t, gotQmv0, "qmv0 must not be created from broken legacy indices")
            require.Equal(t, []intRequest{11}, axgR5PhysicalFileStorage(t, client))
            axgR5CloseFileStorage(t, ext, client)
            t.Logf("AXG_R7_LEGACY_FAIL_CLOSED_PASS case=%s", tc.name)
        })
    }
}

func TestAXGR7NewQueueAndValidLegacyStillWork(t *testing.T) {
    ctx := context.Background()
    t.Run("clean_new", func(t *testing.T) {
        dir := filepath.Join(t.TempDir(), "new")
        require.NoError(t, os.MkdirAll(dir, 0o700))
        ext, client := axgR5OpenFileStorage(t, dir)
        queue := axgR5NewQueue()
        require.NoError(t, queue.initClient(ctx, client))
        require.NoError(t, queue.Offer(ctx, intRequest(41)))
        axgR5CloseFileStorage(t, ext, client)
        ext, client = axgR5OpenFileStorage(t, dir)
        recovered := axgR5NewQueue()
        require.NoError(t, recovered.initClient(ctx, client))
        require.Equal(t, []intRequest{41}, axgDurableInventory(t, recovered))
        axgR5CloseFileStorage(t, ext, client)
        t.Log("AXG_R7_CLEAN_QUEUE_CONTROL_PASS")
    })
    t.Run("valid_legacy", func(t *testing.T) {
        dir := filepath.Join(t.TempDir(), "old")
        require.NoError(t, os.MkdirAll(dir, 0o700))
        ext, client := axgR5OpenFileStorage(t, dir)
        require.NoError(t, client.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(0)))
        require.NoError(t, client.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
        require.NoError(t, client.Set(ctx, getItemKey(0), []byte("11")))
        axgR5CloseFileStorage(t, ext, client)
        ext, client = axgR5OpenFileStorage(t, dir)
        queue := axgR5NewQueue()
        require.NoError(t, queue.initClient(ctx, client))
        require.Equal(t, []intRequest{11}, axgDurableInventory(t, queue))
        require.Equal(t, []intRequest{11}, axgR5PhysicalFileStorage(t, client))
        axgR5CloseFileStorage(t, ext, client)
        t.Log("AXG_R7_VALID_LEGACY_CONTROL_PASS")
    })
}

func TestAXGR7OrphanedLegacyDispatchMarkerMustNotBecomeNewQueue(t *testing.T) {
    ctx := context.Background()
    dir := filepath.Join(t.TempDir(), "orphan-di")
    require.NoError(t, os.MkdirAll(dir, 0o700))
    ext, client := axgR5OpenFileStorage(t, dir)
    marker := itemIndexArrayToBytes([]uint64{0})
    require.NoError(t, client.Set(ctx, legacyCurrentlyDispatchedItemsKey, marker))
    require.NoError(t, client.Set(ctx, getItemKey(0), []byte("11")))
    axgR5CloseFileStorage(t, ext, client)

    ext, client = axgR5OpenFileStorage(t, dir)
    queue := axgR5NewQueue()
    err := queue.initClient(ctx, client)
    require.ErrorContains(t, err, "legacy")
    got, getErr := client.Get(ctx, legacyCurrentlyDispatchedItemsKey)
    require.NoError(t, getErr)
    require.True(t, bytes.Equal(marker, got))
    require.Equal(t, []intRequest{11}, axgR5PhysicalFileStorage(t, client))
    qmv0, metaErr := client.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    require.Empty(t, qmv0)
    axgR5CloseFileStorage(t, ext, client)
    t.Log("AXG_R7_ORPHAN_DISPATCH_MARKER_FAIL_CLOSED")
}

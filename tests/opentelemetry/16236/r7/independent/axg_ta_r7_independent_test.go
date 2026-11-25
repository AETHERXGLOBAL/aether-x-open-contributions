// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// AETHER TEST ARCHITECT R7: separately authored, additive failure-oriented
// tests. All storage operations use isolated actual Contrib file_storage/bbolt.
package queue

import (
    "bytes"
    "context"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
    "go.opentelemetry.io/collector/extension/xextension/storage"
)

func axgTAR7Setup(t *testing.T) (string, storage.Extension, storage.Client) {
    t.Helper()
    dir := filepath.Join(t.TempDir(), "real-contrib")
    require.NoError(t, os.MkdirAll(dir, 0700))
    ext, client := axgR5OpenFileStorage(t, dir)
    return dir, ext, client
}

func axgTAR7StoredKeys(t *testing.T, client storage.Client) map[string][]byte {
    t.Helper()
    w, ok := client.(storage.Walker)
    require.True(t, ok, "require real file_storage Walker")
    found := map[string][]byte{}
    require.NoError(t, w.Walk(context.Background(), func(k string, v []byte) ([]*storage.Operation, error) {
        found[k] = append([]byte{}, v...)
        return nil, nil
    }))
    return found
}

func TestAXGTAR7EmptyButPresentLegacyIndices(t *testing.T) {
    cases := []struct{name string; ri, wi []byte}{
        {"empty_ri", []byte{}, bytesForAXGIndex(1)},
        {"empty_wi", bytesForAXGIndex(0), []byte{}},
        {"empty_both", []byte{}, []byte{}},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            ctx := context.Background()
            dir, ext, client := axgTAR7Setup(t)
            require.NoError(t, client.Set(ctx, legacyReadIndexKey, tc.ri))
            require.NoError(t, client.Set(ctx, legacyWriteIndexKey, tc.wi))
            require.NoError(t, client.Set(ctx, getItemKey(0), []byte("11")))
            seeded := axgTAR7StoredKeys(t, client)
            _, riPresent := seeded[legacyReadIndexKey]
            _, wiPresent := seeded[legacyWriteIndexKey]
            axgR5CloseFileStorage(t, ext, client)
            require.True(t, riPresent && wiPresent, "test requires both zero-length markers actually present on disk")
            ext, client = axgR5OpenFileStorage(t, dir)
            q := axgR5NewQueue()
            initErr := q.initClient(ctx, client)
            after := axgTAR7StoredKeys(t, client)
            physical := axgR5PhysicalFileStorage(t, client)
            axgR5CloseFileStorage(t, ext, client)
            require.Error(t, initErr, "present but malformed legacy indices must fail closed")
            require.Equal(t, tc.ri, after[legacyReadIndexKey], "must not erase original ri")
            require.Equal(t, tc.wi, after[legacyWriteIndexKey], "must not erase original wi")
            _, qmvCreated := after[metadataKey]
            require.False(t, qmvCreated, "must not create qmv0")
            require.Equal(t, []intRequest{11}, physical)
        })
    }
}

func TestAXGTAR7OversizedDispatchCountFailClosed(t *testing.T) {
    ctx := context.Background()
    dir, ext, c := axgTAR7Setup(t)
    corruptDI := []byte{0xff,0xff,0xff,0xff}
    require.NoError(t, c.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(0)))
    require.NoError(t, c.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
    require.NoError(t, c.Set(ctx, legacyCurrentlyDispatchedItemsKey, corruptDI))
    require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
    axgR5CloseFileStorage(t, ext, c)
    ext, c = axgR5OpenFileStorage(t, dir)
    err := axgR5NewQueue().initClient(ctx, c)
    got, getErr := c.Get(ctx, legacyCurrentlyDispatchedItemsKey)
    require.NoError(t, getErr)
    m, metaErr := c.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    inv := axgR5PhysicalFileStorage(t, c)
    axgR5CloseFileStorage(t, ext, c)
    require.Error(t, err, "oversized untrusted dispatch count must not be allocated")
    require.True(t, bytes.Equal(corruptDI, got))
    require.Empty(t, m)
    require.Equal(t, []intRequest{11}, inv)
}

func TestAXGTAR7TrailingGarbageInDispatchArrayFailClosed(t *testing.T) {
    ctx := context.Background()
    dir, ext, c := axgTAR7Setup(t)
    corruptDI := append(itemIndexArrayToBytes([]uint64{0}), 0xaa)
    require.NoError(t, c.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(1)))
    require.NoError(t, c.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
    require.NoError(t, c.Set(ctx, legacyCurrentlyDispatchedItemsKey, corruptDI))
    require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
    axgR5CloseFileStorage(t, ext, c)
    ext, c = axgR5OpenFileStorage(t, dir)
    err := axgR5NewQueue().initClient(ctx, c)
    di, getErr := c.Get(ctx, legacyCurrentlyDispatchedItemsKey)
    require.NoError(t, getErr)
    m, metaErr := c.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    inv := axgR5PhysicalFileStorage(t, c)
    axgR5CloseFileStorage(t, ext, c)
    require.Error(t, err, "trailing garbage after encoded dispatch array must fail closed")
    require.True(t, bytes.Equal(corruptDI, di), "original bytes must survive")
    require.Empty(t, m, "no migration on malformed marker")
    require.Equal(t, []intRequest{11}, inv)
}

func TestAXGTAR7OrphanNumericPayloadWithoutAnyMetadata(t *testing.T) {
    ctx := context.Background()
    dir, ext, c := axgTAR7Setup(t)
    require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
    axgR5CloseFileStorage(t, ext, c)
    ext, c = axgR5OpenFileStorage(t, dir)
    q := axgR5NewQueue()
    err := q.initClient(ctx, c)
    m, metaErr := c.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    inv := axgR5PhysicalFileStorage(t, c)
    axgR5CloseFileStorage(t, ext, c)
    require.Error(t, err, "orphan numeric payload must not silently become an empty queue")
    require.Empty(t, m)
    require.Equal(t, []intRequest{11}, inv)
}

func TestAXGTAR7RestartAfterConsolidatedMetadataBeforeLegacyCleanup(t *testing.T) {
    ctx := context.Background()
    dir, ext, c := axgTAR7Setup(t)
    require.NoError(t, c.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(0)))
    require.NoError(t, c.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
    require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
    require.NoError(t, axgR5NewQueue().initClient(ctx, c))
    // Model a stop after successful consolidated metadata write but before
    // deletion of redundant legacy markers. No product source is patched.
    require.NoError(t, c.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(0)))
    require.NoError(t, c.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(1)))
    axgR5CloseFileStorage(t, ext, c)
    ext, c = axgR5OpenFileStorage(t, dir)
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, c))
    logical := axgDurableInventory(t, q)
    physical := axgR5PhysicalFileStorage(t, c)
    axgR5CloseFileStorage(t, ext, c)
    require.Equal(t, []intRequest{11}, logical)
    require.Equal(t, []intRequest{11}, physical)
}

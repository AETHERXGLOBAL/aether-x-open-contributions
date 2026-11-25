// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0
//
// AETHER X GLOBAL / AETHER TEST ARCHITECT / R10 cold-start adversarial tests.
// No engineering candidate changes; preserve failing security/integrity assertions.
package queue

import (
    "bytes"
    "context"
    "os"
    "path/filepath"
    "strconv"
    "testing"
    "time"

    "github.com/stretchr/testify/require"
    "go.opentelemetry.io/collector/extension/xextension/storage"
    "google.golang.org/protobuf/proto"
)

func axgTAR10PhysicalSnapshot(t *testing.T, client storage.Client) map[string][]byte {
    t.Helper()
    walker, ok := client.(storage.Walker)
    require.True(t, ok, "physical presence oracle requires actual file_storage Walker")
    observed := make(map[string][]byte)
    require.NoError(t, walker.Walk(context.Background(), func(key string, value []byte) ([]*storage.Operation, error) {
        observed[key] = bytes.Clone(value)
        return nil, nil
    }))
    return observed
}

func axgTAR10SeedMetadata(t *testing.T, client storage.Client, read, write uint64) []byte {
    t.Helper()
    raw, err := proto.Marshal(&PersistentMetadata{ReadIndex: read, WriteIndex: write})
    require.NoError(t, err)
    require.NoError(t, client.Set(context.Background(), metadataKey, raw))
    return raw
}

// Independently recheck all keys, and use a physical-value/presence oracle
// before and after a failed startup. No success can erase or rewrite evidence.
func TestAXGTAR10PendingInventoryNeverMutatedOnRefusal(t *testing.T) {
    cases := []struct {
        name string
        read, write uint64
        keys []string
    }{
        {"middle_gap", 0, 3, []string{"0", "2"}},
        {"last_gap_nonzero_start", 3, 6, []string{"3", "4"}},
        {"noncanonical_alias_01", 0, 2, []string{"0", "01"}},
        {"extreme_write_index", 1, ^uint64(0), []string{"1"}},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            ctx := context.Background()
            dir := filepath.Join(t.TempDir(), "ta-r10-disk")
            require.NoError(t, os.MkdirAll(dir, 0o700))
            ext, client := axgR5OpenFileStorage(t, dir)
            raw := axgTAR10SeedMetadata(t, client, tc.read, tc.write)
            for _, key := range tc.keys {
                require.NoError(t, client.Set(ctx, key, []byte("11")))
            }
            axgR5CloseFileStorage(t, ext, client)
            ext, client = axgR5OpenFileStorage(t, dir)
            before := axgTAR10PhysicalSnapshot(t, client)
            err := axgR5NewQueue().initClient(ctx, client)
            after := axgTAR10PhysicalSnapshot(t, client)
            actualMeta, metaErr := client.Get(ctx, metadataKey)
            require.NoError(t, metaErr)
            t.Logf("TA_R10_REFUSAL name=%s error=%v before=%d after=%d", tc.name, err, len(before), len(after))
            require.Error(t, err, "a missing physical pending payload must reject before any mutation")
            require.Equal(t, raw, actualMeta, "persisted qmv0 must not be rewritten")
            require.Equal(t, before, after, "all physical entries and values must be unchanged")
            axgR5CloseFileStorage(t, ext, client)
        })
    }
}

// Observational measurement only: do not turn a 256-item local measurement
// into a large-database or concurrency correctness guarantee.
func TestAXGTAR10ActualDiskValid256PendingSubrange(t *testing.T) {
    ctx := context.Background()
    dir := filepath.Join(t.TempDir(), "ta-r10-valid-256")
    require.NoError(t, os.MkdirAll(dir, 0o700))
    ext, client := axgR5OpenFileStorage(t, dir)
    raw := axgTAR10SeedMetadata(t, client, 400, 656)
    for i := uint64(400); i < 656; i++ {
        require.NoError(t, client.Set(ctx, strconv.FormatUint(i, 10), []byte("11")))
    }
    axgR5CloseFileStorage(t, ext, client)
    ext, client = axgR5OpenFileStorage(t, dir)
    before := axgTAR10PhysicalSnapshot(t, client)
    start := time.Now()
    err := axgR5NewQueue().initClient(ctx, client)
    elapsed := time.Since(start)
    after := axgTAR10PhysicalSnapshot(t, client)
    actualMeta, metaErr := client.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    t.Logf("TA_R10_REAL_FILE_STORAGE_256_PENDING duration=%s err=%v entries=%d", elapsed, err, len(after))
    require.NoError(t, err)
    require.Equal(t, raw, actualMeta)
    require.Equal(t, 257, len(before))
    require.Equal(t, before, after)
    axgR5CloseFileStorage(t, ext, client)
}

// Adversarial deterministic TOCTOU: real bbolt backend performs a physical
// deletion immediately after returning the scanned inventory. The queue
// presently has no transactional snapshot/fencing across that boundary.
// This is a deliberate FAIL oracle until an enforceable ownership contract exists.
type axgTAR10PostWalkDelete struct {
    storage.Client
    originalWalker storage.Walker
    changed bool
}
func (client *axgTAR10PostWalkDelete) Walk(ctx context.Context, fn storage.WalkFunc) error {
    if err := client.originalWalker.Walk(ctx, fn); err != nil {
        return err
    }
    client.changed = true
    return client.Client.Delete(ctx, "1")
}

func TestAXGTAR10PostScanMutationCannotAuthorizeStaleQueue(t *testing.T) {
    ctx := context.Background()
    _, ext, client := axgTAR9Open(t)
    axgTAR10SeedMetadata(t, client, 0, 2)
    require.NoError(t, client.Set(ctx, "0", []byte("11")))
    require.NoError(t, client.Set(ctx, "1", []byte("22")))
    original, ok := client.(storage.Walker)
    require.True(t, ok)
    wrapped := &axgTAR10PostWalkDelete{Client: client, originalWalker: original}
    err := axgR5NewQueue().initClient(ctx, wrapped)
    observed := axgTAR10PhysicalSnapshot(t, client)
    t.Logf("TA_R10_POST_SCAN_MUTATION did_delete=%v startup_error=%v remaining_key_1=%v", wrapped.changed, err, observed["1"])
    require.True(t, wrapped.changed, "the intended mutation must actually occur")
    require.NotContains(t, observed, "1", "physical key 1 is absent after adversarial deletion")
    require.Error(t, err, "startup must not accept a stale pending inventory after a concurrent mutation")
    axgR5CloseFileStorage(t, ext, client)
}

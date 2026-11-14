// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// AETHER X GLOBAL Test Architect R8: independent falsification probes.
// This is deliberately separate from the R8 engineering tests.
// Expected negative findings must NOT be suppressed to claim a green suite.
package queue

import (
    "context"
    "errors"
    "fmt"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
    "google.golang.org/protobuf/proto"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/extension/xextension/storage"
)

// Embedding ONLY storage.Client removes optional Walker from the method set.
type axgTAR8NonWalker struct{ storage.Client }

type axgTAR8ErrorWalker struct{ storage.Client }
func (axgTAR8ErrorWalker) Walk(_ context.Context, _ func(string, []byte) ([]*storage.Operation, error)) error {
    return errors.New("AXG_TA_R8_INJECTED_WALK_ERROR")
}

type axgTAR8CountingWalker struct {
    storage.Client
    inner storage.Walker
    seen int
}
func (w *axgTAR8CountingWalker) Walk(ctx context.Context, f func(string, []byte) ([]*storage.Operation, error)) error {
    return w.inner.Walk(ctx, func(key string, value []byte) ([]*storage.Operation, error) {
        w.seen++
        return f(key, value)
    })
}

func axgTAR8Open(t *testing.T) (string, storage.Extension, storage.Client) {
    t.Helper()
    dir := filepath.Join(t.TempDir(), "ta-r8-real-contrib")
    require.NoError(t, os.MkdirAll(dir, 0o700))
    ext, client := axgR5OpenFileStorage(t, dir)
    return dir, ext, client
}

func TestAXGTAR8NonWalkerUnsafeOrphanAndEmptyMarkers(t *testing.T) {
    // This probe is expected to FAIL against R8. The underlying real Contrib
    // file_storage is wrapped as a storage.Client with NO Walker method.
    for _, name := range []string{"orphan_zero", "empty_present_indices"} {
        t.Run(name, func(t *testing.T) {
            ctx := context.Background()
            dir, ext, c := axgTAR8Open(t)
            if name == "empty_present_indices" {
                require.NoError(t, c.Set(ctx, legacyReadIndexKey, []byte{}))
                require.NoError(t, c.Set(ctx, legacyWriteIndexKey, []byte{}))
                markers := axgTAR7StoredKeys(t, c)
                _, riPresent := markers[legacyReadIndexKey]
                _, wiPresent := markers[legacyWriteIndexKey]
                require.True(t, riPresent && wiPresent, "fixture must really persist empty markers")
            }
            require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
            axgR5CloseFileStorage(t, ext, c)

            ext, c = axgR5OpenFileStorage(t, dir)
            q := axgR5NewQueue()
            var contract storage.Client = axgTAR8NonWalker{Client: c}
            _, accidentallyWalker := contract.(storage.Walker)
            require.False(t, accidentallyWalker)
            initErr := q.initClient(ctx, contract)
            if initErr == nil {
                offerErr := q.Offer(ctx, intRequest(41))
                after, readErr := c.Get(ctx, getItemKey(0))
                require.NoError(t, readErr)
                t.Logf("AXG_TA_R8_DATA_LOSS_REPRO case=%s init=nil offer=%v original=11 final=%q", name, offerErr, string(after))
                require.NoError(t, offerErr)
                require.Equal(t, []byte("11"), after, "DURABLE PAYLOAD OVERWRITTEN: storage.Client without Walker silently reset indices")
            }
            axgR5CloseFileStorage(t, ext, c)
            require.Error(t, initErr, "unsafe legacy/orphan state must reject initialization")
        })
    }
}

func TestAXGTAR8NonWalkerCleanQueueControl(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR8Open(t)
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, axgTAR8NonWalker{Client: c}))
    require.NoError(t, q.Offer(ctx, intRequest(41)))
    require.Equal(t, []intRequest{41}, axgR5PhysicalFileStorage(t, c))
    axgR5CloseFileStorage(t, ext, c)
}

func TestAXGTAR8WalkErrorFailsClosedBeforeWrite(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR8Open(t)
    require.NoError(t, c.Set(ctx, getItemKey(0), []byte("11")))
    q := axgR5NewQueue()
    err := q.initClient(ctx, axgTAR8ErrorWalker{Client: c})
    require.ErrorContains(t, err, "inspect legacy metadata")
    require.ErrorContains(t, err, "AXG_TA_R8_INJECTED_WALK_ERROR")
    got, getErr := c.Get(ctx, getItemKey(0))
    require.NoError(t, getErr)
    require.Equal(t, []byte("11"), got)
    meta, metaErr := c.Get(ctx, metadataKey)
    require.NoError(t, metaErr)
    require.Empty(t, meta)
    axgR5CloseFileStorage(t, ext, c)
}

func TestAXGTAR8PlausibleButWrongQmv0RefusesStartup(t *testing.T) {
    // Expected-to-fail adversarial contract: syntactically valid metadata must
    // not make a missing numeric request silently appear to be durable.
    ctx := context.Background()
    _, ext, c := axgTAR8Open(t)
    bad, err := proto.Marshal(&PersistentMetadata{ReadIndex: 0, WriteIndex: 1})
    require.NoError(t, err)
    require.NoError(t, c.Set(ctx, metadataKey, bad))
    q := axgR5NewQueue()
    initErr := q.initClient(ctx, c)
    t.Logf("AXG_TA_R8_PLAUSIBLE_QMV0_READ_WITHOUT_PAYLOAD init=%v", initErr)
    axgR5CloseFileStorage(t, ext, c)
    require.Error(t, initErr, "plausible qmv0 must not certify a missing durable request")
}

func TestAXGTAR8WalkerScanCardinality(t *testing.T) {
    // Measure O(N) startup scan, not a performance SLA or a large-database PASS.
    ctx := context.Background()
    _, ext, c := axgTAR8Open(t)
    const n = 256
    for i := 0; i < n; i++ {
        require.NoError(t, c.Set(ctx, fmt.Sprintf("unrelated-%04d", i), []byte("x")))
    }
    walker, ok := c.(storage.Walker)
    require.True(t, ok)
    wrapped := &axgTAR8CountingWalker{Client: c, inner: walker}
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, wrapped))
    t.Logf("AXG_TA_R8_WALK_SCAN keys_seeded=%d keys_visited=%d", n, wrapped.seen)
    require.GreaterOrEqual(t, wrapped.seen, n, "legacy fallback must scan the entire namespace")
    axgR5CloseFileStorage(t, ext, c)
}

func TestAXGTAR8RealFileStorageNamespaceIsolation(t *testing.T) {
    ctx := context.Background()
    _, ext, c1 := axgTAR8Open(t)
    c2, err := ext.GetClient(ctx, component.KindExporter, component.MustNewID("isolated"), "logs")
    require.NoError(t, err)
    require.NoError(t, c1.Set(ctx, getItemKey(1024), []byte("11")))
    q2 := axgR5NewQueue()
    require.NoError(t, q2.initClient(ctx, c2), "other scoped client's orphan must not reject this clean namespace")
    qmv2, err := c2.Get(ctx, metadataKey)
    require.NoError(t, err)
    require.NotEmpty(t, qmv2)
    qmv1, err := c1.Get(ctx, metadataKey)
    require.NoError(t, err)
    require.Empty(t, qmv1, "other namespace must not write qmv0 here")
    original, err := c1.Get(ctx, getItemKey(1024))
    require.NoError(t, err)
    require.Equal(t, []byte("11"), original)
    require.NoError(t, c2.Close(ctx))
    axgR5CloseFileStorage(t, ext, c1)
}

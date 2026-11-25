// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0
//
// AETHER X GLOBAL / Test Architect / R9 independently authored adversarial probes.
// No production-source modifications. Failing assertions are intentionally preserved.
package queue

import (
    "context"
    "errors"
    "os"
    "path/filepath"
    "sync"
    "sync/atomic"
    "testing"

    "github.com/stretchr/testify/require"
    "go.opentelemetry.io/collector/extension/xextension/storage"
    "google.golang.org/protobuf/proto"
)

func axgTAR9Open(t *testing.T) (string, storage.Extension, storage.Client) {
    t.Helper()
    dir := filepath.Join(t.TempDir(), "ta-r9-filestorage")
    require.NoError(t, os.MkdirAll(dir, 0o700))
    ext, c := axgR5OpenFileStorage(t, dir)
    return dir, ext, c
}

func axgTAR9HasPhysicalKey(t *testing.T, c storage.Client, key string) bool {
    t.Helper()
    w, ok := c.(storage.Walker)
    require.True(t, ok, "real file_storage must implement Walker for independent oracle")
    present := false
    require.NoError(t, w.Walk(context.Background(), func(k string, _ []byte) ([]*storage.Operation, error) {
        if k == key { present = true }
        return nil, nil
    }))
    return present
}

// Existing R8 failure replay; independent physical key oracle, not q.Size() alone.
func TestAXGTAR9NonWalkerOrphanZeroPreserved(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    require.NoError(t, c.Set(ctx, "0", []byte("11")))
    wrapped := axgTAR8NonWalker{Client: c}
    err := axgR5NewQueue().initClient(ctx, wrapped)
    require.Error(t, err, "an orphan at zero must not become a fresh queue")
    got, e := c.Get(ctx, "0")
    require.NoError(t, e)
    require.Equal(t, []byte("11"), got)
    meta, e := c.Get(ctx, metadataKey)
    require.NoError(t, e)
    require.Empty(t, meta)
    axgR5CloseFileStorage(t, ext, c)
}

// The future 1024th slot is verified without 1024 disk writes.
func TestAXGTAR9NonWalkerOrphan1024CollisionPreserved(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    raw, e := proto.Marshal(&PersistentMetadata{ReadIndex: 1024, WriteIndex: 1024})
    require.NoError(t, e)
    require.NoError(t, c.Set(ctx, metadataKey, raw))
    require.NoError(t, c.Set(ctx, "1024", []byte("11")))
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, axgTAR8NonWalker{Client: c}))
    err := q.Offer(ctx, intRequest(41))
    require.Error(t, err, "occupied future write slot must not be overwritten")
    got, e := c.Get(ctx, "1024")
    require.NoError(t, e)
    require.Equal(t, []byte("11"), got)
    require.Equal(t, int64(0), q.Size())
    axgR5CloseFileStorage(t, ext, c)
}

// Unresolved non-Walker capability gap: zero-length values are indistinguishable
// from missing values through storage.Client.Get; require no silent replacement.
func TestAXGTAR9NonWalkerEmptyPresentNumericSlotMustNotOverwrite(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    require.NoError(t, c.Set(ctx, "0", []byte{}))
    require.True(t, axgTAR9HasPhysicalKey(t, c, "0"), "fixture requires an actual present zero-length key")
    q := axgR5NewQueue()
    err := q.initClient(ctx, axgTAR8NonWalker{Client: c})
    require.Error(t, err, "cannot certify a fresh queue with occupied but empty key 0")
    require.True(t, axgTAR9HasPhysicalKey(t, c, "0"), "record existence must survive rejection")
    axgR5CloseFileStorage(t, ext, c)
}

// Missing middle data is not equivalent to the first-key qmv0 check.
func TestAXGTAR9Qmv0MissingMiddlePayloadMustRefuse(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    bad, e := proto.Marshal(&PersistentMetadata{ReadIndex: 0, WriteIndex: 3})
    require.NoError(t, e)
    require.NoError(t, c.Set(ctx, metadataKey, bad))
    require.NoError(t, c.Set(ctx, "0", []byte("11")))
    require.NoError(t, c.Set(ctx, "2", []byte("33")))
    err := axgR5NewQueue().initClient(ctx, c)
    require.Error(t, err, "first key exists, but missing middle key must not silently pass")
    gotMeta, e := c.Get(ctx, metadataKey)
    require.NoError(t, e)
    require.Equal(t, bad, gotMeta)
    first, e := c.Get(ctx, "0")
    require.NoError(t, e)
    last, e := c.Get(ctx, "2")
    require.NoError(t, e)
    require.Equal(t, []byte("11"), first)
    require.Equal(t, []byte("33"), last)
    axgR5CloseFileStorage(t, ext, c)
}

func TestAXGTAR9NonWalkerPresentEmptyLegacyMarkersMustReject(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    require.NoError(t, c.Set(ctx, legacyReadIndexKey, []byte{}))
    require.NoError(t, c.Set(ctx, legacyWriteIndexKey, []byte{}))
    require.True(t, axgTAR9HasPhysicalKey(t, c, legacyReadIndexKey))
    require.True(t, axgTAR9HasPhysicalKey(t, c, legacyWriteIndexKey))
    err := axgR5NewQueue().initClient(ctx, axgTAR8NonWalker{Client: c})
    require.Error(t, err, "ambiguous empty legacy markers must not be overwritten on startup")
    require.True(t, axgTAR9HasPhysicalKey(t, c, legacyReadIndexKey))
    axgR5CloseFileStorage(t, ext, c)
}

type axgTAR9GetFailClient struct {
    storage.Client
    failKey string
    armed bool
}
func (w *axgTAR9GetFailClient) Get(ctx context.Context, key string) ([]byte, error) {
    if w.armed && key == w.failKey { return nil, errors.New("AXG_TA_R9_GET_INJECTED") }
    return w.Client.Get(ctx, key)
}

func TestAXGTAR9GetErrorMustNotAdvanceDurableWrite(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    wrapped := &axgTAR9GetFailClient{Client: c, failKey: "0"}
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, wrapped))
    beforeMeta, e := c.Get(ctx, metadataKey)
    require.NoError(t, e)
    wrapped.armed = true
    err := q.Offer(ctx, intRequest(41))
    require.ErrorContains(t, err, "AXG_TA_R9_GET_INJECTED")
    got, e := c.Get(ctx, "0")
    require.NoError(t, e)
    require.Empty(t, got)
    afterMeta, e := c.Get(ctx, metadataKey)
    require.NoError(t, e)
    require.Equal(t, beforeMeta, afterMeta)
    require.Zero(t, q.Size())
    axgR5CloseFileStorage(t, ext, c)
}

type axgTAR9Barrier struct {
    ready atomic.Int32
    release chan struct{}
}
type axgTAR9RaceClient struct {
    storage.Client
    gate *axgTAR9Barrier
    armed bool
}
func (w *axgTAR9RaceClient) Get(ctx context.Context, key string) ([]byte, error) {
    value, err := w.Client.Get(ctx, key)
    if w.armed && key == "0" && err == nil {
        if w.gate.ready.Add(1) == 2 { close(w.gate.release) }
        select {
        case <-w.gate.release:
        case <-ctx.Done(): return nil, ctx.Err()
        }
    }
    return value, err
}

// Deterministic time-of-check/time-of-use interleaving: two independent
// writers both inspect the same empty physical slot before either Batch.
// The test does NOT claim that storage.Client provides CAS across clients.
func TestAXGTAR9ConcurrentWriterSharedNamespaceMustNotLoseRequest(t *testing.T) {
    ctx := context.Background()
    _, ext, c := axgTAR9Open(t)
    gate := &axgTAR9Barrier{release: make(chan struct{})}
    a := &axgTAR9RaceClient{Client: c, gate: gate}
    b := &axgTAR9RaceClient{Client: c, gate: gate}
    qa, qb := axgR5NewQueue(), axgR5NewQueue()
    require.NoError(t, qa.initClient(ctx, a))
    require.NoError(t, qb.initClient(ctx, b))
    a.armed, b.armed = true, true
    var wg sync.WaitGroup
    wg.Add(2)
    var first, second error
    go func() { defer wg.Done(); first = qa.Offer(ctx, intRequest(11)) }()
    go func() { defer wg.Done(); second = qb.Offer(ctx, intRequest(41)) }()
    wg.Wait()
    t.Logf("TA_R9_CONCURRENT_BOTH_READ_BEFORE_BATCH first=%v second=%v", first, second)
    require.Equal(t, int32(2), gate.ready.Load(), "both independent writers must have read slot zero")
    physical := axgR5PhysicalFileStorage(t, c)
    t.Logf("TA_R9_CONCURRENT_PHYSICAL_INVENTORY=%v", physical)
    require.Equal(t, []intRequest{11, 41}, physical,
        "must not claim shared-namespace two-writer lossless behavior without CAS/ownership")
    axgR5CloseFileStorage(t, ext, c)
}

func TestAXGTAR9ValidTwoPendingQmv0RestartControl(t *testing.T) {
    ctx := context.Background()
    dir, ext, c := axgTAR9Open(t)
    q := axgR5NewQueue()
    require.NoError(t, q.initClient(ctx, c))
    require.NoError(t, q.Offer(ctx, intRequest(11)))
    require.NoError(t, q.Offer(ctx, intRequest(22)))
    axgR5CloseFileStorage(t, ext, c)
    ext, c = axgR5OpenFileStorage(t, dir)
    restarted := axgR5NewQueue()
    require.NoError(t, restarted.initClient(ctx, c))
    require.Equal(t, []intRequest{11, 22}, axgR5PhysicalFileStorage(t, c))
    axgR5CloseFileStorage(t, ext, c)
}

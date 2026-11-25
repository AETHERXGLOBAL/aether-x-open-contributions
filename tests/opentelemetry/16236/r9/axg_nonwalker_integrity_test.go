// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// R9 Engineering regression suite: actual Contrib filestorage/bbolt,
 // retaining independently authored R8 adversarial fixtures unchanged.
package queue

import (
    "context"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
    "google.golang.org/protobuf/proto"
    "go.opentelemetry.io/collector/extension/xextension/storage"
)

func TestAXGR9NonWalkerFirstOrphanFailsClosed(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"orphan-first")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    require.NoError(t,c.Set(ctx,getItemKey(0),[]byte("11")))
    axgR5CloseFileStorage(t,ext,c)

    ext,c=axgR5OpenFileStorage(t,dir)
    var wrapped storage.Client=axgTAR8NonWalker{Client:c}
    q:=axgR5NewQueue()
    err:=q.initClient(ctx,wrapped)
    require.ErrorContains(t,err,"orphan")
    saved,e:=c.Get(ctx,getItemKey(0))
    require.NoError(t,e)
    require.Equal(t,[]byte("11"),saved)
    meta,e:=c.Get(ctx,metadataKey)
    require.NoError(t,e)
    require.Empty(t,meta)
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R9_NONWALKER_ORPHAN_ZERO_STARTUP_REFUSED")
}

func TestAXGR9NonWalkerFutureOrphanSlotNotOverwritten(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"future-orphan")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    require.NoError(t,c.Set(ctx,getItemKey(3),[]byte("99")))
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)

    q:=axgR5NewQueue()
    wrapped:=axgTAR8NonWalker{Client:c}
    require.NoError(t,q.initClient(ctx,wrapped),"no Walker cannot enumerate future orphan at startup")
    for _,req:=range []intRequest{11,22,33} {
        require.NoError(t,q.Offer(ctx,req))
    }
    err:=q.Offer(ctx,intRequest(41))
    require.ErrorContains(t,err,"existing")
    val,e:=c.Get(ctx,getItemKey(3))
    require.NoError(t,e)
    require.Equal(t,[]byte("99"),val,"original numeric record must not be overwritten")
    require.Equal(t,int64(3),q.Size(),"failed Offer must not change in-memory count")
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R9_NONWALKER_ORPHAN_FUTURE_WRITE_REFUSED")
}

func TestAXGR9PlausibleQmv0MissingFirstPayloadRefused(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"plausible-missing")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    encoded,e:=proto.Marshal(&PersistentMetadata{ReadIndex:0,WriteIndex:1})
    require.NoError(t,e)
    require.NoError(t,c.Set(ctx,metadataKey,encoded))
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    err:=axgR5NewQueue().initClient(ctx,c)
    require.ErrorContains(t,err,"missing")
    saved,e:=c.Get(ctx,metadataKey)
    require.NoError(t,e)
    require.Equal(t,encoded,saved,"metadata must remain unchanged on rejection")
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R9_PLAUSIBLE_QMV0_FIRST_KEY_MISSING_REFUSED")
}

func TestAXGR9ValidQmv0AndNonWalkerCleanControls(t *testing.T) {
    ctx:=context.Background()
    t.Run("valid_qmv0",func(t *testing.T){
        dir:=filepath.Join(t.TempDir(),"valid")
        require.NoError(t,os.MkdirAll(dir,0o700))
        ext,c:=axgR5OpenFileStorage(t,dir)
        q:=axgR5NewQueue()
        require.NoError(t,q.initClient(ctx,c))
        require.NoError(t,q.Offer(ctx,intRequest(11)))
        axgR5CloseFileStorage(t,ext,c)
        ext,c=axgR5OpenFileStorage(t,dir)
        q2:=axgR5NewQueue()
        require.NoError(t,q2.initClient(ctx,c))
        require.Equal(t,[]intRequest{11},axgDurableInventory(t,q2))
        axgR5CloseFileStorage(t,ext,c)
        t.Log("AXG_R9_REAL_FILESTORAGE_VALID_QMV0_CONTROL")
    })
    t.Run("clean_nonwalker",func(t *testing.T){
        dir:=filepath.Join(t.TempDir(),"clean")
        require.NoError(t,os.MkdirAll(dir,0o700))
        ext,c:=axgR5OpenFileStorage(t,dir)
        q:=axgR5NewQueue()
        require.NoError(t,q.initClient(ctx,axgTAR8NonWalker{Client:c}))
        require.NoError(t,q.Offer(ctx,intRequest(41)))
        require.Equal(t,[]intRequest{41},axgR5PhysicalFileStorage(t,c))
        axgR5CloseFileStorage(t,ext,c)
        t.Log("AXG_R9_NONWALKER_CLEAN_QUEUE_CONTROL")
    })
}

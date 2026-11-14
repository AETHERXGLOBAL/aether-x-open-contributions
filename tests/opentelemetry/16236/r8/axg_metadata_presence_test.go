// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// R8 engineering negative and legitimate-queue controls are additive; the
// independently authored R7 and R6 Test Architect fixtures remain unchanged.
package queue

import (
    "bytes"
    "context"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
)

func TestAXGR8AbsentIndexWithNumericRequestBeyondZeroFailsClosed(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"orphan")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    require.NoError(t,c.Set(ctx,getItemKey(1024),[]byte("11")))
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    err:=axgR5NewQueue().initClient(ctx,c)
    require.ErrorContains(t,err,"legacy")
    got,readErr:=c.Get(ctx,getItemKey(1024))
    require.NoError(t,readErr)
    require.Equal(t,[]byte("11"),got)
    meta,readMetaErr:=c.Get(ctx,metadataKey)
    require.NoError(t,readMetaErr)
    require.Empty(t,meta)
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R8_ORPHAN_1024_BLOCKED")
}

func TestAXGR8PresentEmptyLegacyDispatchMarkerNotNewQueue(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"empty-di")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    require.NoError(t,c.Set(ctx,legacyCurrentlyDispatchedItemsKey,[]byte{}))
    initial:=axgTAR7StoredKeys(t,c)
    _,present:=initial[legacyCurrentlyDispatchedItemsKey]
    require.True(t,present)
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    err:=axgR5NewQueue().initClient(ctx,c)
    require.ErrorContains(t,err,"legacy")
    after:=axgTAR7StoredKeys(t,c)
    _,stillPresent:=after[legacyCurrentlyDispatchedItemsKey]
    require.True(t,stillPresent)
    _,written:=after[metadataKey]
    require.False(t,written)
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R8_PRESENT_EMPTY_DI_BLOCKED")
}

func TestAXGR8EmptyConsolidatedMetadataHasNoOrphans(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"empty-qmv0")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    q:=axgR5NewQueue()
    require.NoError(t,q.initClient(ctx,c))
    before:=axgTAR7StoredKeys(t,c)
    _,qmv0Exists:=before[metadataKey]
    require.True(t,qmv0Exists,"original queue initialization must write qmv0, even when empty")
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    reopened:=axgR5NewQueue()
    require.NoError(t,reopened.initClient(ctx,c))
    require.Equal(t,int64(0),reopened.Size())
    require.Empty(t,axgR5PhysicalFileStorage(t,c))
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R8_EMPTY_QMV0_CONTROL_PASS")
}

func TestAXGR8LegacyDispatchZeroCountWithTrailingGarbageFailsClosed(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"zero-count-trailing")
    require.NoError(t,os.MkdirAll(dir,0o700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    bad:=[]byte{0,0,0,0,0xee}
    require.NoError(t,c.Set(ctx,legacyReadIndexKey,bytesForAXGIndex(0)))
    require.NoError(t,c.Set(ctx,legacyWriteIndexKey,bytesForAXGIndex(1)))
    require.NoError(t,c.Set(ctx,legacyCurrentlyDispatchedItemsKey,bad))
    require.NoError(t,c.Set(ctx,getItemKey(0),[]byte("11")))
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    err:=axgR5NewQueue().initClient(ctx,c)
    require.ErrorContains(t,err,"legacy")
    got,readErr:=c.Get(ctx,legacyCurrentlyDispatchedItemsKey)
    require.NoError(t,readErr)
    require.True(t,bytes.Equal(bad,got))
    meta,readMetaErr:=c.Get(ctx,metadataKey)
    require.NoError(t,readMetaErr)
    require.Empty(t,meta)
    require.Equal(t,[]intRequest{11},axgR5PhysicalFileStorage(t,c))
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R8_ZERO_COUNT_TRAILING_DI_BLOCKED")
}

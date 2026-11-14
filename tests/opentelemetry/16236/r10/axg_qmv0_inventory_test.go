// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// R10 bounded engineering regressions. Independent R9 tests remain untouched.
package queue

import (
    "bytes"
    "context"
    "math"
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/require"
    "google.golang.org/protobuf/proto"
    "go.opentelemetry.io/collector/extension/xextension/storage"
)

func axgR10Meta(t *testing.T, c storage.Client, read, write uint64) []byte {
    t.Helper()
    buf, err := proto.Marshal(&PersistentMetadata{ReadIndex: read, WriteIndex: write})
    require.NoError(t, err)
    require.NoError(t, c.Set(context.Background(), metadataKey, buf))
    return buf
}

func TestAXGR10MissingPendingPayloadsRefuseWithoutMutation(t *testing.T) {
    for _, tc := range []struct{
        name string
        read,write uint64
        present map[string][]byte
        nonWalker bool
    }{
        {"missing_middle",0,3,map[string][]byte{"0":[]byte("11"),"2":[]byte("33")},false},
        {"missing_last",0,3,map[string][]byte{"0":[]byte("11"),"1":[]byte("22")},false},
        {"noncanonical_alias_not_enough",0,2,map[string][]byte{"0":[]byte("11"),"01":[]byte("22")},false},
        {"missing_middle_nonwalker",0,3,map[string][]byte{"0":[]byte("11"),"2":[]byte("33")},true},
        {"implausibly_large_metadata",0,math.MaxUint64,map[string][]byte{"0":[]byte("11")},false},
    } {
        t.Run(tc.name,func(t *testing.T) {
            ctx:=context.Background()
            dir:=filepath.Join(t.TempDir(),"actual-contrib")
            require.NoError(t,os.MkdirAll(dir,0700))
            ext,c:=axgR5OpenFileStorage(t,dir)
            raw:=axgR10Meta(t,c,tc.read,tc.write)
            for k,v:=range tc.present { require.NoError(t,c.Set(ctx,k,v)) }
            axgR5CloseFileStorage(t,ext,c)
            ext,c=axgR5OpenFileStorage(t,dir)
            var client storage.Client=c
            if tc.nonWalker { client=axgTAR8NonWalker{Client:c} }
            err:=axgR5NewQueue().initClient(ctx,client)
            require.ErrorContains(t,err,"missing")
            still,e:=c.Get(ctx,metadataKey)
            require.NoError(t,e)
            require.True(t,bytes.Equal(raw,still),"no metadata reset or rewrite on corrupt startup")
            for k,v:=range tc.present {
                got,e:=c.Get(ctx,k)
                require.NoError(t,e)
                require.True(t,bytes.Equal(v,got),"physical request preserved at %q",k)
            }
            axgR5CloseFileStorage(t,ext,c)
            t.Logf("AXG_R10_QMV0_MISSING_FAIL_CLOSED case=%s",tc.name)
        })
    }
}

func TestAXGR10ValidPendingSubrangeRestart(t *testing.T) {
    ctx:=context.Background()
    dir:=filepath.Join(t.TempDir(),"qmv0-valid")
    require.NoError(t,os.MkdirAll(dir,0700))
    ext,c:=axgR5OpenFileStorage(t,dir)
    raw:=axgR10Meta(t,c,1,3)
    for k,v:=range map[string][]byte{"1":[]byte("22"),"2":[]byte("33")} {
        require.NoError(t,c.Set(ctx,k,v))
    }
    axgR5CloseFileStorage(t,ext,c)
    ext,c=axgR5OpenFileStorage(t,dir)
    q:=axgR5NewQueue()
    require.NoError(t,q.initClient(ctx,c))
    got,e:=c.Get(ctx,metadataKey)
    require.NoError(t,e)
    require.True(t,bytes.Equal(raw,got))
    require.Equal(t,[]intRequest{22,33},axgR5PhysicalFileStorage(t,c))
    axgR5CloseFileStorage(t,ext,c)
    t.Log("AXG_R10_QMV0_VALID_SUBRANGE_RESTART_PASS")
}

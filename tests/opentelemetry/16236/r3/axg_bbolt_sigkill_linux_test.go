// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Linux-only isolated real-process SIGKILL qualification with an actual bbolt
// on-disk transactional database. The storage adapter uses the same bbolt
// Update(Batch ops...) semantics as contrib's filestorage/client.go, but this
// is NOT a test of the complete contrib file_storage extension or Collector.
package queue

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"syscall"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	"go.etcd.io/bbolt"
	"go.opentelemetry.io/collector/extension/xextension/storage"
)

var axgBoltBucket = []byte("default")

type axgBoltClient struct {
	db        *bbolt.DB
	killAfter int
	committed int
}

func axgOpenBolt(t *testing.T, path string, killAfter int) *axgBoltClient {
	t.Helper()
	db, err := bbolt.Open(path, 0o600, &bbolt.Options{
		Timeout: 2 * time.Second,
		NoSync: false, // fsync enabled, like production filestorage FSync=true.
		NoFreelistSync: true,
		FreelistType: bbolt.FreelistMapType,
	})
	require.NoError(t, err)
	require.NoError(t, db.Update(func(tx *bbolt.Tx) error {
		_, e := tx.CreateBucketIfNotExists(axgBoltBucket)
		return e
	}))
	return &axgBoltClient{db: db, killAfter: killAfter}
}

func (c *axgBoltClient) Get(ctx context.Context, key string) ([]byte, error) {
	op := storage.GetOperation(key)
	if err := c.Batch(ctx, op); err != nil {
		return nil, err
	}
	return op.Value, nil
}
func (c *axgBoltClient) Set(ctx context.Context, key string, value []byte) error {
	return c.Batch(ctx, storage.SetOperation(key, value))
}
func (c *axgBoltClient) Delete(ctx context.Context, key string) error {
	return c.Batch(ctx, storage.DeleteOperation(key))
}
func (c *axgBoltClient) Close(context.Context) error { return c.db.Close() }

func (c *axgBoltClient) Batch(_ context.Context, ops ...*storage.Operation) error {
	retired := false
	err := c.db.Update(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket(axgBoltBucket)
		if bucket == nil {
			return errors.New("missing bbolt default bucket")
		}
		for _, op := range ops {
			switch op.Type {
			case storage.Get:
				op.Value = append([]byte(nil), bucket.Get([]byte(op.Key))...)
			case storage.Set:
				if e := bucket.Put([]byte(op.Key), op.Value); e != nil { return e }
			case storage.Delete:
				if op.Key == "0" || op.Key == "1" { retired = true }
				if e := bucket.Delete([]byte(op.Key)); e != nil { return e }
			default:
				return fmt.Errorf("invalid storage op %d", op.Type)
			}
		}
		return nil
	})
	if err != nil { return err }
	if c.killAfter > 0 && retired {
		c.committed++
		if c.committed == c.killAfter {
			// Real SIGKILL at the *post-commit* boundary, not a panic and
			// not a timer-based kill. No Go defers or clean shutdown run.
			_ = syscall.Kill(os.Getpid(), syscall.SIGKILL)
			return errors.New("SIGKILL unexpectedly returned")
		}
	}
	return nil
}

func TestAXGBboltChild(t *testing.T) {
	mode := os.Getenv("AXG_BBOLT_MODE")
	if mode == "" { t.Skip("subprocess-only test") }
	path := os.Getenv("AXG_BBOLT_PATH")
	if path == "" { t.Fatal("missing isolated database path") }
	killAfter := 0
	if mode == "crash" { killAfter = 1 }
	if mode == "crash_second" { killAfter = 2 }
	client := axgOpenBolt(t, path, killAfter)
	defer client.Close(context.Background())

	switch mode {
	case "seed":
		axgSeedNative(t, client, false)
	case "seed_legacy":
		axgSeedNative(t, client, true)
	case "crash", "crash_second":
		// The old and candidate source both run this exact upstream method.
		_ = createTestPersistentQueueWithClient(client)
		t.Fatal("no SIGKILL after required committed retirement transaction")
	default:
		t.Fatalf("unknown subprocess mode %q", mode)
	}
}

// Both existing fixture helpers accept *axgCommittedStore. For the native
// bbolt fixture, write the exact metadata layout through queue methods here.
func axgSeedNative(t *testing.T, client *axgBoltClient, legacy bool) {
	t.Helper()
	ctx := context.Background()
	if legacy {
		require.NoError(t, client.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(2)))
		require.NoError(t, client.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(3)))
		require.NoError(t, client.Set(ctx, legacyCurrentlyDispatchedItemsKey, itemIndexArrayToBytes([]uint64{0,1})))
		for i, value := range []string{"11","22","33"} {
			require.NoError(t, client.Set(ctx, getItemKey(uint64(i)), []byte(value)))
		}
		return
	}
	queue := createTestPersistentQueueWithClient(client)
	for _, v := range []intRequest{11,22,33} {
		require.NoError(t, queue.Offer(ctx, v))
	}
	for _, want := range []intRequest{11,22} {
		_, got, _, ok := queue.Read(ctx)
		require.True(t, ok)
		require.Equal(t, want, got)
	}
}

func bytesForAXGIndex(index uint64) []byte {
	// Legacy indices are little-endian uint64.
	b := make([]byte, 8)
	for i := 0; i < 8; i++ { b[i] = byte(index >> (8*i)) }
	return b
}

func axgRunBoltChild(t *testing.T, path, mode string, shouldKill bool) {
	t.Helper()
	cmd := exec.Command(os.Args[0], "-test.run=^TestAXGBboltChild$", "-test.v")
	cmd.Env = append(os.Environ(), "AXG_BBOLT_MODE="+mode, "AXG_BBOLT_PATH="+path)
	out, err := cmd.CombinedOutput()
	if !shouldKill {
		require.NoErrorf(t, err, "mode %s: %s", mode, string(out))
		return
	}
	var exitErr *exec.ExitError
	require.ErrorAsf(t, err, &exitErr, "mode %s did not die: %s", mode, string(out))
	ws, ok := exitErr.Sys().(syscall.WaitStatus)
	require.True(t, ok, "expected OS wait status")
	require.Truef(t, ws.Signaled() && ws.Signal()==syscall.SIGKILL,
		"mode=%s exited without SIGKILL: status=%v stdout=%s", mode, ws, string(out))
	t.Logf("AXG_BBOLT_SIGKILL_CONFIRMED mode=%s", mode)
}

func axgCheckBboltInventory(t *testing.T, path string) {
	t.Helper()
	client := axgOpenBolt(t,path,0)
	defer client.Close(context.Background())
	queue := createTestPersistentQueueWithClient(client)
	vals := axgDurableInventory(t,queue)
	sort.Slice(vals,func(i,j int)bool{return vals[i]<vals[j]})
	require.Equal(t,[]intRequest{11,22,33},vals)
	require.Empty(t,queue.metadata.CurrentlyDispatchedItems)
	t.Logf("AXG_BBOLT_RESTART_PRESERVED ids=%v",vals)
}

func TestAXGBboltSIGKILLRecovery(t *testing.T) {
	for _, tc := range []struct {
		name, seed, kill string
	}{
		{name:"qmv0_first_committed",seed:"seed",kill:"crash"},
		{name:"qmv0_second_committed",seed:"seed",kill:"crash_second"},
		{name:"legacy_first_committed",seed:"seed_legacy",kill:"crash"},
	} {
		t.Run(tc.name,func(t *testing.T){
			dbPath := filepath.Join(t.TempDir(),"axg-bbolt.db")
			axgRunBoltChild(t,dbPath,tc.seed,false)
			axgRunBoltChild(t,dbPath,tc.kill,true)
			axgCheckBboltInventory(t,dbPath)
		})
	}
}

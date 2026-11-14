// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Internal R6 bounded reliability tests. All process kills run in subprocesses
// with temporary real Contrib file_storage databases, never against production.
package queue

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"syscall"
	"testing"

	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/collector/extension/xextension/storage"
	"go.opentelemetry.io/collector/exporter/exporterhelper/internal/request"
)

type axgR6InjectedBatch struct {
	storage.Client
	mode string
	hit  bool
}

func (w *axgR6InjectedBatch) Batch(ctx context.Context, ops ...*storage.Operation) error {
	if !w.hit {
		for _, op := range ops {
			if op.Type == storage.Delete && (op.Key == "0" || op.Key == "1") {
				w.hit = true
				switch w.mode {
				case "precommit":
					return fmt.Errorf("AXG_R6_PRECOMMIT_STORAGE_FULL: %w", storage.ErrStorageFull)
				case "postcommit":
					if err := w.Client.Batch(ctx, ops...); err != nil {
						return err
					}
					return errors.New("AXG_R6_AMBIGUOUS_ERROR_AFTER_COMMITTED_BATCH")
				case "kill":
					if err := w.Client.Batch(ctx, ops...); err != nil {
						return err
					}
					// Real OS-level SIGKILL AFTER the Contrib storage
					// client's Batch returned. Do not call Go cleanup.
					_ = syscall.Kill(os.Getpid(), syscall.SIGKILL)
					return errors.New("SIGKILL unexpectedly returned")
				default:
					return fmt.Errorf("unsupported fault mode %q", w.mode)
				}
			}
		}
	}
	return w.Client.Batch(ctx, ops...)
}

func axgR6Seed(t *testing.T, c storage.Client, legacy bool) {
	t.Helper()
	ctx := context.Background()
	if legacy {
		require.NoError(t, c.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(2)))
		require.NoError(t, c.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(3)))
		require.NoError(t, c.Set(ctx, legacyCurrentlyDispatchedItemsKey, itemIndexArrayToBytes([]uint64{0, 1})))
		for i, val := range []string{"11", "22", "33"} {
			require.NoError(t, c.Set(ctx, getItemKey(uint64(i)), []byte(val)))
		}
		return
	}
	q := axgR5NewQueue()
	require.NoError(t, q.initClient(ctx, c))
	for _, v := range []intRequest{11, 22, 33} {
		require.NoError(t, q.Offer(ctx, v))
	}
	for _, expected := range []intRequest{11, 22} {
		_, v, _, ok := q.Read(ctx)
		require.True(t, ok)
		require.Equal(t, expected, v)
	}
}

func axgR6OpenAndInventory(t *testing.T, dir string) ([]intRequest, []intRequest) {
	t.Helper()
	ext, c := axgR5OpenFileStorage(t, dir)
	q := axgR5NewQueue()
	require.NoError(t, q.initClient(context.Background(), c))
	logical := axgDurableInventory(t, q)
	physical := axgR5PhysicalFileStorage(t, c)
	axgR5CloseFileStorage(t, ext, c)
	return logical, physical
}

func axgR6RequireInventory(t *testing.T, dir string, expected []intRequest) {
	t.Helper()
	logical, physical := axgR6OpenAndInventory(t, dir)
	sort.Slice(logical, func(i, j int) bool { return logical[i] < logical[j] })
	sort.Slice(physical, func(i, j int) bool { return physical[i] < physical[j] })
	require.Equal(t, expected, logical, "queue-visible inventory mismatch")
	require.Equal(t, expected, physical, "actual storage physical inventory mismatch or duplicate")
}

func TestAXGR6RealFileStorageInjectedPrecommitENOSPC(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "injected-full")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ext, c := axgR5OpenFileStorage(t, dir)
	axgR6Seed(t, c, false)
	axgR5CloseFileStorage(t, ext, c)

	ext, c = axgR5OpenFileStorage(t, dir)
	w := &axgR6InjectedBatch{Client: c, mode: "precommit"}
	q := axgR5NewQueue()
	err := q.initClient(context.Background(), w)
	require.ErrorIs(t, err, storage.ErrStorageFull)
	require.True(t, w.hit)
	axgR5CloseFileStorage(t, ext, c)
	axgR6RequireInventory(t, dir, []intRequest{11, 22, 33})
	t.Log("AXG_R6_CONTRIB_PRECOMMIT_FULL_FAIL_CLOSED_PRESERVED")
	// This is fault injection, not an actual ENOSPC filesystem event.
}

func TestAXGR6RealFileStorageAmbiguousErrorAfterCommit(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "ambiguous-commit")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ext, c := axgR5OpenFileStorage(t, dir)
	axgR6Seed(t, c, false)
	axgR5CloseFileStorage(t, ext, c)

	ext, c = axgR5OpenFileStorage(t, dir)
	w := &axgR6InjectedBatch{Client: c, mode: "postcommit"}
	q := axgR5NewQueue()
	err := q.initClient(context.Background(), w)
	require.ErrorContains(t, err, "AXG_R6_AMBIGUOUS_ERROR_AFTER_COMMITTED_BATCH")
	require.True(t, w.hit)
	axgR5CloseFileStorage(t, ext, c)
	// The storage Batch actually committed, but the caller saw error.
	// Recovery must use durable metadata on reopen, not stale memory.
	axgR6RequireInventory(t, dir, []intRequest{11, 22, 33})
	t.Log("AXG_R6_CONTRIB_POSTCOMMIT_AMBIGUOUS_REOPEN_PRESERVED")
}

func TestAXGR6AckedVsUnackedDeliveryBoundaries(t *testing.T) {
	for _, tc := range []struct {
		name string
		ackFirst bool
		expect []intRequest
	}{
		{name: "acked_first_is_not_replayed", ackFirst: true, expect: []intRequest{22, 33}},
		{name: "unacked_first_may_be_replayed", ackFirst: false, expect: []intRequest{11, 22, 33}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			dir := filepath.Join(t.TempDir(), "delivery-ack")
	require.NoError(t, os.MkdirAll(dir, 0o700))
			ext, c := axgR5OpenFileStorage(t, dir)
			q := axgR5NewQueue()
			require.NoError(t, q.initClient(context.Background(), c))
			for _, item := range []intRequest{11, 22, 33} {
				require.NoError(t, q.Offer(context.Background(), item))
			}
			_, item, done, ok := q.Read(context.Background())
			require.True(t, ok)
			require.Equal(t, intRequest(11), item)
			if tc.ackFirst {
				// Acknowledgement is durably persisted before restart.
				done.OnDone(nil)
			} // Otherwise emulate delivery with no durable ack.
			axgR5CloseFileStorage(t, ext, c)
			axgR6RequireInventory(t, dir, tc.expect)
			t.Logf("AXG_R6_ACK_BOUNDARY_OK case=%s expected=%v", tc.name, tc.expect)
		})
	}
	t.Log("AXG_R6_NO_EXACTLY_ONCE_CLAIM: unacknowledged delivery replays by design")
}

func TestAXGR6DurableFullCapacityAfterRecovery(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "full-capacity")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ext, c := axgR5OpenFileStorage(t, dir)
	q := newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 3)).(*persistentQueue[intRequest])
	require.NoError(t, q.initClient(context.Background(), c))
	for _, item := range []intRequest{11, 22, 33} {
		require.NoError(t, q.Offer(context.Background(), item))
	}
	for _, item := range []intRequest{11, 22} {
		_, got, _, ok := q.Read(context.Background())
		require.True(t, ok)
		require.Equal(t, item, got)
	}
	axgR5CloseFileStorage(t, ext, c)

	ext, c = axgR5OpenFileStorage(t, dir)
	recovered := newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 3)).(*persistentQueue[intRequest])
	require.NoError(t, recovered.initClient(context.Background(), c))
	require.Equal(t, int64(3), recovered.Size())
	require.ErrorIs(t, recovered.Offer(context.Background(), intRequest(44)), ErrQueueIsFull)
	require.Equal(t, []intRequest{11, 22, 33}, axgR5PhysicalFileStorage(t, c))
	axgR5CloseFileStorage(t, ext, c)
	t.Log("AXG_R6_FULL_CAPACITY_RESTART_PRESERVED_AND_REJECTED_NEW_OFFER")
}

func TestAXGR6ExtensionChildSIGKILL(t *testing.T) {
	mode := os.Getenv("AXG_R6_CHILD_MODE")
	if mode == "" { t.Skip("subprocess-only test") }
	dir := os.Getenv("AXG_R6_CHILD_DIR")
	if dir == "" { t.Fatal("missing isolated directory") }

	ext, c := axgR5OpenFileStorage(t, dir)
	switch mode {
	case "seed":
		axgR6Seed(t, c, false)
		axgR5CloseFileStorage(t, ext, c)
	case "seed_legacy":
		axgR6Seed(t, c, true)
		axgR5CloseFileStorage(t, ext, c)
	case "crash":
		w := &axgR6InjectedBatch{Client: c, mode: "kill"}
		q := axgR5NewQueue()
		_ = q.initClient(context.Background(), w)
		t.Fatal("expected OS SIGKILL after successful actual extension Batch")
	default:
		t.Fatalf("unexpected subprocess mode %q", mode)
	}
}

func axgR6RunExtensionChild(t *testing.T, dir, mode string, expectKill bool) {
	t.Helper()
	cmd := exec.Command(os.Args[0], "-test.run=^TestAXGR6ExtensionChildSIGKILL$", "-test.v")
	cmd.Env = append(os.Environ(), "AXG_R6_CHILD_MODE="+mode, "AXG_R6_CHILD_DIR="+dir)
	out, err := cmd.CombinedOutput()
	if !expectKill {
		require.NoErrorf(t, err, "child %s: %s", mode, string(out))
		return
	}
	var exit *exec.ExitError
	require.ErrorAs(t, err, &exit, "expected subprocess signal")
	wait, ok := exit.Sys().(syscall.WaitStatus)
	require.True(t, ok)
	require.Truef(t, wait.Signaled() && wait.Signal()==syscall.SIGKILL,
		"expected SIGKILL after actual Contrib Batch, got %v; output=%s", wait, string(out))
	t.Log("AXG_R6_ACTUAL_CONTRIB_PROCESS_SIGKILL_CONFIRMED")
}

func TestAXGR6ActualFileStoragePostCommitSIGKILL(t *testing.T) {
	for _, tc := range []struct{name,seed string}{
		{name:"qmv0",seed:"seed"},
		{name:"legacy",seed:"seed_legacy"},
	} {
		t.Run(tc.name,func(t *testing.T){
			dir := filepath.Join(t.TempDir(), strings.ToLower(tc.name))
		require.NoError(t, os.MkdirAll(dir, 0o700))
			axgR6RunExtensionChild(t, dir, tc.seed, false)
			axgR6RunExtensionChild(t, dir, "crash", true)
			axgR6RequireInventory(t, dir, []intRequest{11, 22, 33})
			t.Logf("AXG_R6_REAL_CONTRIB_SIGKILL_RECOVERED case=%s", tc.name)
		})
	}
}

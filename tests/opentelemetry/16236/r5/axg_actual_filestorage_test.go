// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// R5: exercise the actual OpenTelemetry Collector Contrib file_storage factory,
// extension lifecycle, GetClient namespacing, bbolt persistence and Walker.
package queue

import (
	"bytes"
	"context"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"testing"

	"github.com/open-telemetry/opentelemetry-collector-contrib/extension/storage/filestorage"
	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/collector/component"
	"go.opentelemetry.io/collector/extension/extensiontest"
	"go.opentelemetry.io/collector/extension/xextension/storage"
)

func axgR5OpenFileStorage(t *testing.T, directory string) (storage.Extension, storage.Client) {
	t.Helper()
	ctx := context.Background()
	factory := filestorage.NewFactory()
	cfg := factory.CreateDefaultConfig().(*filestorage.Config)
	cfg.Directory = directory
	cfg.FSync = true
	cfg.Compaction.OnStart = false
	cfg.Compaction.OnRebound = false
	extension, err := factory.Create(ctx, extensiontest.NewNopSettings(factory.Type()), cfg)
	require.NoError(t, err)
	require.NoError(t, extension.Start(ctx, nil))
	asStorage, ok := extension.(storage.Extension)
	require.True(t, ok, "must use actual storage.Extension, not a handwritten bbolt client")
	client, err := asStorage.GetClient(ctx, component.KindExporter, component.MustNewID("otlp"), "logs")
	require.NoError(t, err)
	return asStorage, client
}

func axgR5CloseFileStorage(t *testing.T, ext storage.Extension, client storage.Client) {
	t.Helper()
	require.NoError(t, client.Close(context.Background()))
	require.NoError(t, ext.Shutdown(context.Background()))
}

func axgR5PhysicalFileStorage(t *testing.T, client storage.Client) []intRequest {
	t.Helper()
	walker, ok := client.(storage.Walker)
	require.True(t, ok, "actual file_storage must expose Walker for independent physical inventory")
	out := make([]intRequest, 0)
	require.NoError(t, walker.Walk(context.Background(), func(key string, raw []byte) ([]*storage.Operation, error) {
		if _, err := strconv.ParseUint(key, 10, 64); err != nil {
			return nil, nil
		}
		_, item, err := (int64Encoding{}).Unmarshal(raw)
		if err != nil {
			return nil, err
		}
		out = append(out, item)
		return nil, nil
	}))
	sort.Slice(out, func(i, j int) bool { return out[i] < out[j] })
	return out
}

func TestAXGR5FileStorageActualExtensionRestartNoLoss(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "actual-file-storage")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ctx := context.Background()
	ext, client := axgR5OpenFileStorage(t, dir)
	queue := createTestPersistentQueueWithClient(client)
	for _, value := range []intRequest{11, 22, 33} {
		require.NoError(t, queue.Offer(ctx, value))
	}
	for _, want := range []intRequest{11, 22} {
		_, got, _, ok := queue.Read(ctx)
		require.True(t, ok)
		require.Equal(t, want, got)
	}
	axgR5CloseFileStorage(t, ext, client)

	restartExt, restartClient := axgR5OpenFileStorage(t, dir)
	restarted := createTestPersistentQueueWithClient(restartClient)
	require.Equal(t, []intRequest{11, 22, 33}, axgDurableInventory(t, restarted))
	require.Equal(t, []intRequest{11, 22, 33}, axgR5PhysicalFileStorage(t, restartClient))
	axgR5CloseFileStorage(t, restartExt, restartClient)
	t.Log("AXG_R5_REAL_FILESTORAGE_QMV0_RESTART_PASS")
}

func TestAXGR5FileStorageActualExtensionLegacyMigration(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "actual-file-storage-legacy")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ctx := context.Background()
	ext, client := axgR5OpenFileStorage(t, dir)
	require.NoError(t, client.Set(ctx, legacyReadIndexKey, bytesForAXGIndex(2)))
	require.NoError(t, client.Set(ctx, legacyWriteIndexKey, bytesForAXGIndex(3)))
	require.NoError(t, client.Set(ctx, legacyCurrentlyDispatchedItemsKey, itemIndexArrayToBytes([]uint64{0, 1})))
	for i, val := range []string{"11", "22", "33"} {
		require.NoError(t, client.Set(ctx, getItemKey(uint64(i)), []byte(val)))
	}
	axgR5CloseFileStorage(t, ext, client)

	restartExt, restartClient := axgR5OpenFileStorage(t, dir)
	restarted := createTestPersistentQueueWithClient(restartClient)
	require.Equal(t, []intRequest{11, 22, 33}, axgDurableInventory(t, restarted))
	require.Equal(t, []intRequest{11, 22, 33}, axgR5PhysicalFileStorage(t, restartClient))
	axgR5CloseFileStorage(t, restartExt, restartClient)
	t.Log("AXG_R5_REAL_FILESTORAGE_LEGACY_PASS")
}

func TestAXGR5FileStorageActualExtensionCorruptQmv0FailClosed(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "actual-file-storage-corrupt")
	require.NoError(t, os.MkdirAll(dir, 0o700))
	ctx := context.Background()
	ext, client := axgR5OpenFileStorage(t, dir)
	q := createTestPersistentQueueWithClient(client)
	for _, value := range []intRequest{11, 22} {
		require.NoError(t, q.Offer(ctx, value))
	}
	good, err := client.Get(ctx, metadataKey)
	require.NoError(t, err)
	bad := []byte{0xff, 0xff, 0xff}
	require.NoError(t, client.Set(ctx, metadataKey, bad))
	axgR5CloseFileStorage(t, ext, client)

	reopenedExt, reopenedClient := axgR5OpenFileStorage(t, dir)
	attempt := axgR5NewQueue()
	err = attempt.initClient(ctx, reopenedClient)
	require.ErrorContains(t, err, "metadata")
	got, err := reopenedClient.Get(ctx, metadataKey)
	require.NoError(t, err)
	require.True(t, bytes.Equal(bad, got))
	require.Equal(t, []intRequest{11, 22}, axgR5PhysicalFileStorage(t, reopenedClient))
	axgR5CloseFileStorage(t, reopenedExt, reopenedClient)

	restoredExt, restoredClient := axgR5OpenFileStorage(t, dir)
	require.NoError(t, restoredClient.Set(ctx, metadataKey, good))
	restored := createTestPersistentQueueWithClient(restoredClient)
	require.Equal(t, []intRequest{11, 22}, axgDurableInventory(t, restored))
	require.Equal(t, []intRequest{11, 22}, axgR5PhysicalFileStorage(t, restoredClient))
	axgR5CloseFileStorage(t, restoredExt, restoredClient)
	t.Log("AXG_R5_REAL_FILESTORAGE_CORRUPT_QMV0_FAIL_CLOSED")
}

// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Internal R5 safety tests: corrupt qmv0 MUST not silently reset durable
// indices or overwrite stored payloads. This is not recovery from arbitrary
// metadata corruption, and no external production claim is made.
package queue

import (
	"bytes"
	"context"
	"errors"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/collector/exporter/exporterhelper/internal/request"
	"go.opentelemetry.io/collector/extension/xextension/storage"
	"google.golang.org/protobuf/proto"
)

func axgR5NewQueue() *persistentQueue[intRequest] {
	return newPersistentQueue[intRequest](newSettingsWithStorage(request.SizerTypeRequests, 1000)).(*persistentQueue[intRequest])
}

func TestAXGR5CorruptQmv0FailsClosedAndPreservesDisk(t *testing.T) {
	ctx := context.Background()
	path := filepath.Join(t.TempDir(), "corrupt-qmv0.db")
	initial := axgOpenBolt(t, path, 0)
	queue := createTestPersistentQueueWithClient(initial)
	require.NoError(t, queue.Offer(ctx, intRequest(11)))
	require.NoError(t, queue.Offer(ctx, intRequest(22)))
	good, err := initial.Get(ctx, metadataKey)
	require.NoError(t, err)
	require.NotEmpty(t, good)
	require.Equal(t, []intRequest{11, 22}, axgIndependentPhysicalInventory(t, initial))
	invalid := []byte{0xff, 0xff, 0xff}
	require.NoError(t, initial.Set(ctx, metadataKey, invalid))
	require.NoError(t, initial.Close(ctx))

	broken := axgOpenBolt(t, path, 0)
	start := axgR5NewQueue()
	err = start.initClient(ctx, broken)
	require.Error(t, err, "corrupt metadata must not be interpreted as a new empty queue")
	require.ErrorContains(t, err, "metadata")
	got, err := broken.Get(ctx, metadataKey)
	require.NoError(t, err)
	require.True(t, bytes.Equal(invalid, got), "failed startup must never replace corrupt metadata")
	require.Equal(t, []intRequest{11, 22}, axgIndependentPhysicalInventory(t, broken))
	require.NoError(t, broken.Close(ctx))
	t.Log("AXG_R5_CORRUPT_QMV0_FAIL_CLOSED_PRESERVED")

	// A deliberate operator restoration of the original good metadata
	// establishes that refusal to start did not destroy the payloads.
	repair := axgOpenBolt(t, path, 0)
	require.NoError(t, repair.Set(ctx, metadataKey, good))
	recovered := axgR5NewQueue()
	require.NoError(t, recovered.initClient(ctx, repair))
	require.Equal(t, []intRequest{11, 22}, axgDurableInventory(t, recovered))
	require.Equal(t, []intRequest{11, 22}, axgIndependentPhysicalInventory(t, repair))
	require.NoError(t, repair.Close(ctx))
	t.Log("AXG_R5_QMV0_MANUAL_RESTORE_SUCCESS")
}

type axgR5ReadErrorClient struct {
	storage.Client
}

func (c axgR5ReadErrorClient) Get(ctx context.Context, key string) ([]byte, error) {
	if key == metadataKey {
		return nil, errors.New("AXG_R5_INJECTED_QMV0_READ_FAILURE")
	}
	return c.Client.Get(ctx, key)
}

func TestAXGR5MetadataReadErrorFailsClosed(t *testing.T) {
	ctx := context.Background()
	path := filepath.Join(t.TempDir(), "read-error.db")
	seed := axgOpenBolt(t, path, 0)
	queue := createTestPersistentQueueWithClient(seed)
	require.NoError(t, queue.Offer(ctx, intRequest(11)))
	require.NoError(t, seed.Close(ctx))

	client := axgOpenBolt(t, path, 0)
	before, err := client.Get(ctx, metadataKey)
	require.NoError(t, err)
	init := axgR5NewQueue()
	err = init.initClient(ctx, axgR5ReadErrorClient{Client: client})
	require.ErrorContains(t, err, "AXG_R5_INJECTED_QMV0_READ_FAILURE")
	after, err := client.Get(ctx, metadataKey)
	require.NoError(t, err)
	require.True(t, bytes.Equal(before, after))
	require.Equal(t, []intRequest{11}, axgIndependentPhysicalInventory(t, client))
	require.NoError(t, client.Close(ctx))
	t.Log("AXG_R5_METADATA_IO_ERROR_FAIL_CLOSED")
}

func TestAXGR5ImpossibleMetadataIndicesFailClosed(t *testing.T) {
	ctx := context.Background()
	path := filepath.Join(t.TempDir(), "bad-indices.db")
	client := axgOpenBolt(t, path, 0)
	original := createTestPersistentQueueWithClient(client)
	require.NoError(t, original.Offer(ctx, intRequest(11)))
	require.NoError(t, original.Offer(ctx, intRequest(22)))
	invalid := &PersistentMetadata{ReadIndex: 9, WriteIndex: 2}
	invalidBytes, err := proto.Marshal(invalid)
	require.NoError(t, err)
	require.NoError(t, client.Set(ctx, metadataKey, invalidBytes))
	require.NoError(t, client.Close(ctx))

	reopened := axgOpenBolt(t, path, 0)
	newQueue := axgR5NewQueue()
	err = newQueue.initClient(ctx, reopened)
	require.Error(t, err, "read index past write index is logically inconsistent")
	require.ErrorContains(t, err, "metadata")
	raw, err := reopened.Get(ctx, metadataKey)
	require.NoError(t, err)
	require.True(t, bytes.Equal(invalidBytes, raw))
	require.Equal(t, []intRequest{11, 22}, axgIndependentPhysicalInventory(t, reopened))
	require.NoError(t, reopened.Close(ctx))
	t.Log("AXG_R5_IMPOSSIBLE_INDICES_FAIL_CLOSED")
}

func TestAXGR5MissingMetadataStillInitializesNewQueue(t *testing.T) {
	ctx := context.Background()
	path := filepath.Join(t.TempDir(), "new-empty.db")
	client := axgOpenBolt(t, path, 0)
	queue := axgR5NewQueue()
	require.NoError(t, queue.initClient(ctx, client),
		"a never-initialized storage client must remain supported")
	require.NoError(t, queue.Offer(ctx, intRequest(41)))
	require.Equal(t, []intRequest{41}, axgDurableInventory(t, queue))
	require.NoError(t, client.Close(ctx))
	t.Log("AXG_R5_NEW_EMPTY_QUEUE_CONTROL_PASS")
}

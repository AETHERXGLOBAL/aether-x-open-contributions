// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

// Candidate regression for open-telemetry/opentelemetry-collector#15966.
// This test drives Graph.Build, rather than invoking warnIfDoubleBatching
// directly on hand-constructed graph nodes. Unexecuted until replayed in
// the exact upstream service module; not a claim of upstream acceptance.
package graph

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"go.uber.org/zap/zaptest/observer"

	"go.opentelemetry.io/collector/component"
	"go.opentelemetry.io/collector/component/componenttest"
	"go.opentelemetry.io/collector/config/configoptional"
	"go.opentelemetry.io/collector/connector"
	"go.opentelemetry.io/collector/consumer"
	"go.opentelemetry.io/collector/exporter"
	"go.opentelemetry.io/collector/exporter/exporterhelper"
	"go.opentelemetry.io/collector/pdata/pmetric"
	"go.opentelemetry.io/collector/pipeline"
	"go.opentelemetry.io/collector/processor"
	"go.opentelemetry.io/collector/receiver"
	"go.opentelemetry.io/collector/service/internal/builders"
	"go.opentelemetry.io/collector/service/internal/testcomponents"
	"go.opentelemetry.io/collector/service/pipelines"
)

type aetherPassThroughMetrics struct {
	consumer.Metrics
}

func (*aetherPassThroughMetrics) Start(context.Context, component.Host) error { return nil }
func (*aetherPassThroughMetrics) Shutdown(context.Context) error              { return nil }

func TestAetherGraphBuildDoubleBatchingWarningIsPipelineScoped(t *testing.T) {
	batchType := component.MustNewType("batch")
	batchID := component.NewID(batchType)
	batchFactory := processor.NewFactory(
		batchType,
		func() component.Config { return struct{}{} },
		processor.WithMetrics(
			func(_ context.Context, _ processor.Settings, _ component.Config, next consumer.Metrics) (processor.Metrics, error) {
				return &aetherPassThroughMetrics{Metrics: next}, nil
			},
			component.StabilityLevelAlpha,
		),
	)

	exporterType := component.MustNewType("aetherexp")
	enabledID := component.NewIDWithName(exporterType, "batched")
	disabledID := component.NewIDWithName(exporterType, "unbatched")
	exporterFactory := exporter.NewFactory(
		exporterType,
		func() component.Config { return struct{}{} },
		exporter.WithMetrics(
			func(ctx context.Context, set exporter.Settings, cfg component.Config) (exporter.Metrics, error) {
				queueCfg := exporterhelper.NewDefaultQueueConfig()
				queueCfg.Batch = configoptional.None[exporterhelper.BatchConfig]()
				if set.ID == enabledID {
					queueCfg.Batch = configoptional.Some(exporterhelper.NewDefaultBatchConfig())
				}
				queue := configoptional.Some(queueCfg)
				return exporterhelper.NewMetrics(ctx, set, cfg, func(context.Context, pmetric.Metrics) error { return nil },
					exporterhelper.WithQueue(queue))
			},
			component.StabilityLevelAlpha,
		),
	)

	recvFactory := testcomponents.ExampleReceiverFactory
	recvType := recvFactory.Type()
	recv1 := component.NewIDWithName(recvType, "affected")
	recv2 := component.NewIDWithName(recvType, "no-legacy-batch")
	recv3 := component.NewIDWithName(recvType, "queue-only")
	affected := pipeline.NewIDWithName(pipeline.SignalMetrics, "affected")
	noLegacy := pipeline.NewIDWithName(pipeline.SignalMetrics, "no-legacy-batch")
	queueOnly := pipeline.NewIDWithName(pipeline.SignalMetrics, "queue-only")

	core, logs := observer.New(zapcore.WarnLevel)
	telemetry := componenttest.NewNopTelemetrySettings()
	telemetry.Logger = zap.New(core)
	cfgs := pipelines.Config{
		affected: {
			Receivers:  []component.ID{recv1},
			Processors: []component.ID{batchID},
			Exporters:  []component.ID{enabledID},
		},
		noLegacy: {
			Receivers: []component.ID{recv2},
			Exporters: []component.ID{enabledID},
		},
		queueOnly: {
			Receivers:  []component.ID{recv3},
			Processors: []component.ID{batchID},
			Exporters:  []component.ID{disabledID},
		},
	}
	graph, err := Build(context.Background(), Settings{
		Telemetry: telemetry,
		BuildInfo: component.NewDefaultBuildInfo(),
		ReceiverBuilder: builders.NewReceiver(
			map[component.ID]component.Config{
				recv1: recvFactory.CreateDefaultConfig(),
				recv2: recvFactory.CreateDefaultConfig(),
				recv3: recvFactory.CreateDefaultConfig(),
			},
			map[component.Type]receiver.Factory{recvType: recvFactory},
		),
		ProcessorBuilder: builders.NewProcessor(
			map[component.ID]component.Config{batchID: batchFactory.CreateDefaultConfig()},
			map[component.Type]processor.Factory{batchType: batchFactory},
		),
		ExporterBuilder: builders.NewExporter(
			map[component.ID]component.Config{
				enabledID:  exporterFactory.CreateDefaultConfig(),
				disabledID: exporterFactory.CreateDefaultConfig(),
			},
			map[component.Type]exporter.Factory{exporterType: exporterFactory},
		),
		ConnectorBuilder: builders.NewConnector(
			map[component.ID]component.Config{},
			map[component.Type]connector.Factory{},
		),
		PipelineConfigs: cfgs,
	})
	require.NoError(t, err)
	require.NotNil(t, graph)

	warnings := logs.FilterMessageSnippet("double batching").All()
	require.Len(t, warnings, 1, "only the affected pipeline should emit a warning")
	require.Equal(t, affected.String(), warnings[0].ContextMap()["pipeline"])
	require.Equal(t, enabledID.String(), warnings[0].ContextMap()["exporter"])
}

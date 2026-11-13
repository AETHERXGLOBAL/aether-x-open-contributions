#!/usr/bin/env python3
"""Read-only structural audit of an exact, independently fetched upstream source file.

This is NOT an OpenTelemetry integration/regression test. It establishes only
that the observed ID plumbing matches the hypothesis in upstream issue #16398.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def inspect(text: str) -> dict:
    m = re.search(r'func exporterSettings\(set processor\.Settings\) exporter\.Settings \{(?P<body>.*?)\n\}', text, re.S)
    if not m:
        raise AssertionError('exporterSettings not found: inspect source manually')
    body = m.group('body')
    assert re.search(r'\bID:\s+set\.ID\s*,', body), 'No direct ID set.ID assignment found'
    assert not re.search(r'(PipelineID|PipelineName|InstanceID)', body), 'Pipeline- or instance-derived ID found: re-evaluate'
    names = ['newTracesProcessor', 'newMetricsProcessor', 'newLogsProcessor', 'newProfilesProcessor']
    present = {}
    for name in names:
        match = re.search(rf'func {name}\(.*?(?=\nfunc |\Z)', text, re.S)
        present[name] = bool(match and 'exporterSettings(set)' in match.group())
        assert present[name], f'expected exporterSettings(set) in {name}'
    return {
        'direct_id_assignment': True,
        'pipeline_or_instance_override_in_exporterSettings': False,
        'signals_using_exporterSettings': present,
        'scope': 'source-only structural check; no persistence test or runtime reproduction',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--expected-sha256', required=True)
    args = parser.parse_args()
    data = Path(args.source).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == args.expected_sha256, 'source bytes mismatch'
    result = inspect(data.decode('utf-8'))
    print(json.dumps({'verdict': 'SOURCE_STATIC_MATCH', 'source_sha256': digest, **result}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

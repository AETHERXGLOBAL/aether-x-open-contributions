#!/usr/bin/env python3
"""F03 measured end-to-end schema cost; descriptive metrics, not an acceptance threshold."""
from __future__ import annotations

import gc
import json
import statistics
import sys
import time
import tracemalloc

from pydantic import ConfigDict, TypeAdapter, __version__
from typing_extensions import TypedDict


class Leaf(TypedDict):
    value: str


def measure(n: int, distinct: bool) -> dict:
    fields: dict[str, type] = {}
    for index in range(n):
        parent = TypedDict(f'P_{n}_{distinct}_{index}', {'child': Leaf})
        parent.__pydantic_config__ = (
            ConfigDict(str_min_length=index + 1)
            if distinct
            else ConfigDict(extra='ignore')
        )
        fields[f'field_{index}'] = parent
    root = TypedDict(f'Root_{n}_{distinct}', fields)
    gc.collect()
    tracemalloc.start()
    started = time.perf_counter()
    adapter = TypeAdapter(root)
    json_schema = adapter.json_schema()
    elapsed_ms = (time.perf_counter() - started) * 1000
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        'elapsed_ms': round(elapsed_ms, 3),
        'peak_kib': round(peak_bytes / 1024, 2),
        'json_defs': len(json_schema.get('$defs', {})),
    }


def main() -> int:
    measurements = []
    for distinct in (False, True):
        for n in (16, 32, 64):
            samples = [measure(n, distinct) for _ in range(2)]
            measurements.append({
                'mode': 'distinct_contexts' if distinct else 'equivalent_contexts',
                'fields': n,
                'median_elapsed_ms': round(statistics.median(v['elapsed_ms'] for v in samples), 3),
                'median_peak_kib': round(statistics.median(v['peak_kib'] for v in samples), 2),
                'json_defs': samples[0]['json_defs'],
                'samples': samples,
            })
    print(json.dumps({
        'status': 'MEASURED_NOT_PERFORMANCE_APPROVED',
        'python': sys.version.split()[0],
        'pydantic': __version__,
        'scope': 'TypeAdapter + JSON schema; 2 samples; local CI runner only',
        'measurements': measurements,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

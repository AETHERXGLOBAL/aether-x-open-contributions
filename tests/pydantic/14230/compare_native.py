#!/usr/bin/env python3
"""Compare exact native Pydantic pytest JUnit outcomes before/after a candidate.

This does NOT treat pre-existing official-main failures as candidate regressions.
It rejects disappearing/added cases, parser ambiguity and any newly failing test.
"""
import argparse
import json
from pathlib import Path
from xml.etree import ElementTree


def collect(path: Path) -> dict[tuple[str, str], str]:
    root = ElementTree.parse(path).getroot()
    results: dict[tuple[str, str], str] = {}
    for case in root.iter('testcase'):
        key = (case.attrib.get('classname', ''), case.attrib.get('name', ''))
        if not all(key) or key in results:
            raise ValueError(f'Invalid or duplicate native testcase identity: {key}')
        kind = 'FAIL' if any(child.tag in ('error', 'failure') for child in case) else (
            'SKIP' if any(child.tag == 'skipped' for child in case) else 'PASS'
        )
        results[key] = kind
    if not results:
        raise ValueError(f'No native testcases parsed from {path}')
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline_xml', type=Path)
    parser.add_argument('patched_xml', type=Path)
    args = parser.parse_args()
    baseline = collect(args.baseline_xml)
    patched = collect(args.patched_xml)
    names_match = baseline.keys() == patched.keys()
    base_bad = {k for k, v in baseline.items() if v == 'FAIL'}
    new_bad = {k for k, v in patched.items() if v == 'FAIL'} - base_bad
    fixed = base_bad - {k for k, v in patched.items() if v == 'FAIL'}
    new_skip = {k for k, v in patched.items() if v == 'SKIP' and baseline[k] != 'SKIP'}
    record = {
        'baseline_total': len(baseline),
        'patched_total': len(patched),
        'baseline_failures': len(base_bad),
        'patched_failures': sum(v == 'FAIL' for v in patched.values()),
        'testcase_identities_identical': names_match,
        'new_failures': [':'.join(k) for k in sorted(new_bad)],
        'new_skips': [':'.join(k) for k in sorted(new_skip)],
        'resolved_baseline_failures': [':'.join(k) for k in sorted(fixed)],
        'outcome': 'PASS_NO_NEW_FAILURES' if names_match and not new_bad and not new_skip else 'BLOCK',
        'note': 'An existing upstream baseline failure remains a failure; this checks delta only.',
    }
    print(json.dumps(record, sort_keys=True, indent=2))
    return 0 if record['outcome'] == 'PASS_NO_NEW_FAILURES' else 1


if __name__ == '__main__':
    raise SystemExit(main())

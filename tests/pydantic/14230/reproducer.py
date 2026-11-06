#!/usr/bin/env python3
"""Reproducible, read-only Pydantic #14230 regression oracle.

Dependencies: pydantic v2; Python 3.11+; typing_extensions (Pydantic dependency).
Modes:
  --expect-bug  : PASS only if independent controls succeed and both root orderings
                  demonstrate shared-child configuration leakage.
  --require-fix : PASS only if independent controls and BOTH root orderings
                  preserve the inherited configuration per occurrence.
Not an upstream acceptance test, patch, or evidence against current main.
"""
import argparse
import json
import sys
from typing_extensions import TypedDict

from pydantic import ConfigDict, TypeAdapter, __version__ as pydantic_version


class Item(TypedDict):
    name: str


class Permissive(TypedDict):
    __pydantic_config__ = ConfigDict(extra="allow")
    item: Item


class Restrictive(TypedDict):
    __pydantic_config__ = ConfigDict(extra="ignore")
    item: Item


class Root(TypedDict):
    permissive: Permissive
    restrictive: Restrictive


class RootReversed(TypedDict):
    restrictive: Restrictive
    permissive: Permissive


def run(mode: str) -> tuple[int, dict]:
    sample = {"item": {"name": "abcd", "extra": 1}}
    input_root = {"permissive": sample, "restrictive": sample}
    allowed = {"item": {"name": "abcd", "extra": 1}}
    restricted = {"item": {"name": "abcd"}}
    expected_root = {"permissive": allowed, "restrictive": restricted}

    observed = {
        "permissive_alone": TypeAdapter(Permissive).validate_python(sample),
        "restrictive_alone": TypeAdapter(Restrictive).validate_python(sample),
        "root_permissive_first": TypeAdapter(Root).validate_python(input_root),
        "root_restrictive_first": TypeAdapter(RootReversed).validate_python(input_root),
    }
    controls_pass = (
        observed["permissive_alone"] == allowed
        and observed["restrictive_alone"] == restricted
    )
    forward_ok = observed["root_permissive_first"] == expected_root
    reverse_ok = observed["root_restrictive_first"] == expected_root
    characteristic_bug = (
        observed["root_permissive_first"] == {"permissive": allowed, "restrictive": allowed}
        and observed["root_restrictive_first"] == {"permissive": restricted, "restrictive": restricted}
    )

    passed = controls_pass and (
        characteristic_bug if mode == "expect-bug" else (forward_ok and reverse_ok)
    )
    report = {
        "issue": "pydantic/pydantic#14230",
        "test_context": "installed_distribution_only; not upstream main qualification",
        "python_version": sys.version.split()[0],
        "pydantic_version": pydantic_version,
        "mode": mode,
        "controls_pass": controls_pass,
        "forward_root_expected": forward_ok,
        "reverse_root_expected": reverse_ok,
        "characteristic_order_dependent_bug": characteristic_bug,
        "result": "PASS" if passed else "FAIL",
        "observed": observed,
        "expected_root": expected_root,
    }
    return (0 if passed else 1), report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--expect-bug", action="store_true")
    group.add_argument("--require-fix", action="store_true")
    args = parser.parse_args()
    code, report = run("expect-bug" if args.expect_bug else "require-fix")
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())

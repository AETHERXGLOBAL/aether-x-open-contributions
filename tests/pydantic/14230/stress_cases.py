#!/usr/bin/env python3
"""Independent nested-container, strict-extra and ref-reuse oracle for issue #14230.

Run `--expect-bug` on unmodified source and `--require-fix` on a candidate.
Each case has a separately documented expected output; no upstream changes.
"""
from __future__ import annotations

import argparse
import json

from pydantic import ConfigDict, TypeAdapter, ValidationError
from typing_extensions import TypedDict


class Leaf(TypedDict):
    value: int


class ListAllow(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    items: list[Leaf]


class ListIgnore(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    items: list[Leaf]


class ListRoot(TypedDict):
    allow: ListAllow
    ignore: ListIgnore


class MapAllow(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    items: dict[str, Leaf]


class MapIgnore(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    items: dict[str, Leaf]


class MapRoot(TypedDict):
    allow: MapAllow
    ignore: MapIgnore


class Forbidden(TypedDict):
    __pydantic_config__ = ConfigDict(extra='forbid')
    item: Leaf


class Allowed(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    item: Leaf


class ForbidRoot(TypedDict):
    allow: Allowed
    forbid: Forbidden


class EqualA(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    item: Leaf


class EqualB(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    item: Leaf


class EqualRoot(TypedDict):
    a: EqualA
    b: EqualB


def run() -> dict[str, bool]:
    list_input = {
        'allow': {'items': [{'value': 3, 'extra': 1}]},
        'ignore': {'items': [{'value': 4, 'extra': 2}]},
    }
    list_expected = {
        'allow': {'items': [{'value': 3, 'extra': 1}]},
        'ignore': {'items': [{'value': 4}]},
    }
    list_adapter = TypeAdapter(ListRoot)
    list_ok = (
        list_adapter.validate_python(list_input) == list_expected
        and list_adapter.validate_json(json.dumps(list_input)) == list_expected
    )
    map_input = {
        'allow': {'items': {'k': {'value': 3, 'extra': 1}}},
        'ignore': {'items': {'k': {'value': 4, 'extra': 2}}},
    }
    map_expected = {
        'allow': {'items': {'k': {'value': 3, 'extra': 1}}},
        'ignore': {'items': {'k': {'value': 4}}},
    }
    map_adapter = TypeAdapter(MapRoot)
    map_ok = (
        map_adapter.validate_python(map_input) == map_expected
        and map_adapter.validate_json(json.dumps(map_input)) == map_expected
    )
    forbidden_input = {
        'allow': {'item': {'value': 1, 'extra': 9}},
        'forbid': {'item': {'value': 2, 'extra': 9}},
    }
    try:
        TypeAdapter(ForbidRoot).validate_python(forbidden_input)
    except ValidationError as error:
        forbid_ok = any(
            tuple(entry['loc']) == ('forbid', 'item', 'extra')
            and entry['type'] == 'extra_forbidden'
            for entry in error.errors()
        )
    else:
        forbid_ok = False

    equal_input = {
        'a': {'item': {'value': 2, 'extra': 7}},
        'b': {'item': {'value': 3, 'extra': 8}},
    }
    equal_adapter = TypeAdapter(EqualRoot)
    equal_result = equal_adapter.validate_python(equal_input)
    defs = equal_adapter.json_schema().get('$defs', {})
    same_config_ok = (
        equal_result == {'a': {'item': {'value': 2}}, 'b': {'item': {'value': 3}}}
        and sum(v.get('title') == 'Leaf' for v in defs.values()) == 1
    )
    return {
        'nested_list_inheritance': list_ok,
        'nested_mapping_inheritance': map_ok,
        'forbid_extra_path': forbid_ok,
        'same_config_single_reference': same_config_ok,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('--expect-bug', action='store_true')
    grp.add_argument('--require-fix', action='store_true')
    flags = parser.parse_args()
    checks = run()
    expected = (
        {
            'nested_list_inheritance': False,
            'nested_mapping_inheritance': False,
            'forbid_extra_path': False,
            'same_config_single_reference': True,
        } if flags.expect_bug else {key: True for key in checks}
    )
    passed = checks == expected
    print(json.dumps({'checks': checks, 'expected': expected, 'passed': passed}, indent=2, sort_keys=True))
    raise SystemExit(0 if passed else 1)

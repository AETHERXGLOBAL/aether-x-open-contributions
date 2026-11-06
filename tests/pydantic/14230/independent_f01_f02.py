#!/usr/bin/env python3
"""Exact-source integration falsifiers for Pydantic #14230 candidate.patch.

F01: valid JSON-schema callback with user-defined equality that raises RuntimeError.
F02: default and explicit extra='ignore' must not duplicate identical leaf schemas.
Run with an unmodified checked-out Pydantic and again after the exact candidate patch.
A failure is a hard negative result, NOT an accepted engineering change.
"""
import json
import sys

from pydantic import ConfigDict, TypeAdapter, __version__ as pydantic_version
from typing_extensions import TypedDict


class EqualityBomb:
    def __call__(self, schema: dict) -> None:
        schema['x-f01'] = 'callback-executed'

    def __eq__(self, other: object) -> bool:
        raise RuntimeError('AXG_F01_USER_EQUALITY_RAISED')


class Leaf(TypedDict):
    name: str


class ExtraCallbackA(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow', json_schema_extra=EqualityBomb())
    item: Leaf


class ExtraCallbackB(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow', json_schema_extra=EqualityBomb())
    item: Leaf


class CallbackRoot(TypedDict):
    a: ExtraCallbackA
    b: ExtraCallbackB


class DefaultExtra(TypedDict):
    __pydantic_config__ = ConfigDict()
    item: Leaf


class ExplicitIgnore(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    item: Leaf


class EquivalentRoot(TypedDict):
    a: DefaultExtra
    b: ExplicitIgnore


def f01() -> dict:
    try:
        adapter = TypeAdapter(CallbackRoot)
        result = adapter.validate_python({'a': {'item': {'name': 'A'}}, 'b': {'item': {'name': 'B'}}})
        expected = {'a': {'item': {'name': 'A'}}, 'b': {'item': {'name': 'B'}}}
        return {'pass': result == expected, 'observation': 'validation returned', 'result': result}
    except Exception as exc:
        return {'pass': False, 'exception': type(exc).__name__, 'message': str(exc)[:200]}


def f02() -> dict:
    try:
        adapter = TypeAdapter(EquivalentRoot)
        data = {'a': {'item': {'name': 'A'}}, 'b': {'item': {'name': 'B'}}}
        validated = adapter.validate_python(data)
        schema = adapter.json_schema()
        matching = sorted(name for name, definition in schema.get('$defs', {}).items() if definition.get('title') == 'Leaf')
        return {
            'pass': validated == data and len(matching) == 1,
            'schema_leaf_ref_names': matching,
            'duplicate_leaf_definitions': max(0, len(matching) - 1),
        }
    except Exception as exc:
        return {'pass': False, 'exception': type(exc).__name__, 'message': str(exc)[:200]}


def main() -> int:
    checks = {'F01_untrusted_config_equality': f01(), 'F02_equivalent_effective_config': f02()}
    passed = all(value['pass'] for value in checks.values())
    print(json.dumps({
        'source': 'runtime import must be separately pinned and verified',
        'pydantic_version': pydantic_version,
        'checks': checks,
        'outcome': 'PASS_NO_F01_F02' if passed else 'BLOCK_F01_F02',
    }, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())

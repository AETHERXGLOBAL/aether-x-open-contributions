#!/usr/bin/env python3
"""R2 candidate-only invariant tests (not an independent assurance report)."""
from __future__ import annotations

import json
from typing import Generic, TypeVar

from pydantic import ConfigDict, TypeAdapter, ValidationError
from pydantic._internal._generate_schema import _Definitions
from typing_extensions import TypedDict

T = TypeVar('T')


class IntLeaf(TypedDict):
    value: int


class Strict(TypedDict):
    __pydantic_config__ = ConfigDict(strict=True)
    child: IntLeaf


class Lax(TypedDict):
    __pydantic_config__ = ConfigDict(strict=False)
    child: IntLeaf


class StrictRoot(TypedDict):
    strict: Strict
    lax: Lax


class GenericLeaf(TypedDict, Generic[T]):
    value: T


class AllowGeneric(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    child: GenericLeaf[str]


class IgnoreGeneric(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    child: GenericLeaf[str]


class GenericRoot(TypedDict):
    allow: AllowGeneric
    ignore: IgnoreGeneric


class Untrusted:
    __hash__ = None

    def __eq__(self, other: object) -> bool:
        raise RuntimeError('UNTRUSTED_EQUALITY_RAN')


def main() -> int:
    default_key = _Definitions._inherited_td_config_key(ConfigDict())
    explicit_ignore_key = _Definitions._inherited_td_config_key(ConfigDict(extra='ignore'))
    explicit_default_key = _Definitions._inherited_td_config_key(ConfigDict(strict=False))
    strict_key = _Definitions._inherited_td_config_key(ConfigDict(strict=True))

    exotic = Untrusted()
    cyclic: dict[str, object] = {}
    cyclic['cycle'] = cyclic
    unusual_key = _Definitions._inherited_td_config_key(
        ConfigDict(plugin_settings={'callback': exotic, 'cyclic': cyclic})
    )
    repeated_key = _Definitions._inherited_td_config_key(
        ConfigDict(plugin_settings={'callback': exotic, 'cyclic': cyclic})
    )

    adapter = TypeAdapter(StrictRoot)
    strict_input = {'strict': {'child': {'value': '7'}}, 'lax': {'child': {'value': '8'}}}
    try:
        adapter.validate_python(strict_input)
    except ValidationError as exc:
        strict_rejected = any(
            tuple(error['loc']) == ('strict', 'child', 'value')
            for error in exc.errors()
        )
    else:
        strict_rejected = False

    valid = adapter.validate_python(
        {'strict': {'child': {'value': 7}}, 'lax': {'child': {'value': '8'}}}
    )
    generic_adapter = TypeAdapter(GenericRoot)
    input_value = {
        'allow': {'child': {'value': 'a', 'extra': 1}},
        'ignore': {'child': {'value': 'b', 'extra': 2}},
    }
    generic_value = generic_adapter.validate_python(input_value)
    generic_schema = generic_adapter.json_schema()
    checks = {
        'default_and_explicit_ignore_key': default_key == explicit_ignore_key,
        'explicit_false_default_key': default_key == explicit_default_key,
        'different_strict_keys': default_key != strict_key,
        'identity_and_cycle_safe': unusual_key == repeated_key,
        'strict_nested_validation_rejects_string': strict_rejected,
        'lax_nested_validation_coerces_string': valid['lax']['child']['value'] == 8,
        'generic_typeddict_contexts': generic_value == {
            'allow': {'child': {'value': 'a', 'extra': 1}},
            'ignore': {'child': {'value': 'b'}},
        },
        'generic_json_schema_nonempty': bool(generic_schema),
    }
    print(json.dumps({'checks': checks, 'pass': all(checks.values())}, sort_keys=True, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())

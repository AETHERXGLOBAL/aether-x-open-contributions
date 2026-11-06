#!/usr/bin/env python3
"""Adversarial TypedDict config-propagation tests for Pydantic #14230.

This test is internal evidence, not a Pydantic upstream test or accepted patch.
It exercises repeated parent contexts, explicit child config, and recursion.
"""
import json
from typing_extensions import NotRequired, TypedDict
from pydantic import ConfigDict, TypeAdapter, __version__ as pydantic_version


class Shared(TypedDict):
    name: str


class A1(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    item: Shared


class B1(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    item: Shared


class A2(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    item: Shared


class B2(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    item: Shared


class RootMany(TypedDict):
    a1: A1
    b1: B1
    a2: A2
    b2: B2


class Explicit(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    name: str


class ExplicitAllowParent(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    item: Explicit


class ExplicitForbidParent(TypedDict):
    __pydantic_config__ = ConfigDict(extra='forbid')
    item: Explicit


class ExplicitRoot(TypedDict):
    a: ExplicitAllowParent
    b: ExplicitForbidParent


class Node(TypedDict):
    name: str
    next: NotRequired['Node']


class TreeAllow(TypedDict):
    __pydantic_config__ = ConfigDict(extra='allow')
    node: Node


class TreeIgnore(TypedDict):
    __pydantic_config__ = ConfigDict(extra='ignore')
    node: Node


class TreeRoot(TypedDict):
    a: TreeAllow
    b: TreeIgnore


def main() -> int:
    item = {'item': {'name': 'a', 'extra': 1}}
    names = ('a1', 'b1', 'a2', 'b2')
    observed_many = TypeAdapter(RootMany).validate_python({k: item for k in names})
    expected_many = {
        k: {'item': {'name': 'a', **({'extra': 1} if k.startswith('a') else {})}} for k in names
    }

    explicit_item = {'item': {'name': 'b', 'extra': 2}}
    observed_explicit = TypeAdapter(ExplicitRoot).validate_python({'a': explicit_item, 'b': explicit_item})
    expected_explicit = {'a': {'item': {'name': 'b'}}, 'b': {'item': {'name': 'b'}}}

    node = {'name': 'n', 'extra': 9, 'next': {'name': 'leaf', 'extra': 8}}
    observed_tree = TypeAdapter(TreeRoot).validate_python({'a': {'node': node}, 'b': {'node': node}})
    expected_tree = {
        'a': {'node': node},
        'b': {'node': {'name': 'n', 'next': {'name': 'leaf'}}},
    }
    checks = {
        'alternating_inherited_contexts': observed_many == expected_many,
        'explicit_child_override': observed_explicit == expected_explicit,
        'recursive_inherited_contexts': observed_tree == expected_tree,
    }
    print(json.dumps({
        'pydantic_version': pydantic_version,
        'checks': checks,
        'all_pass': all(checks.values()),
        'observed': {
            'many': observed_many,
            'explicit': observed_explicit,
            'tree': observed_tree,
        },
    }, sort_keys=True, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())

from enum import IntEnum
from typing import Any, Optional, Type
from unittest import TestCase

from framework.lang.dict import pluck
from framework.lang.object import Assigner
from tests.helper.fixture import data_provider


class EnumA(IntEnum):
    A = 1
    B = 2
    C = 3


class ClassA:
    a: int = 0
    b: str = ''
    c: Optional[int] = None
    e: EnumA = EnumA.A


class TestObject(TestCase):
    @data_provider([
        ({'a': 1, 'b': 'string', 'e': 3}, ClassA),
        ({'a': 1, 'b': 'string', 'c': 2, 'e': 3}, ClassA),
    ])
    def test_assigner(self, data: dict, assign_type: Type):
        actual = Assigner.assign(assign_type, data)
        for key, value in data.items():
            self.assertEquals(getattr(actual, key), value)

    @data_provider([
        ({'a': 1}, 'a', 1),
        ({'a': {'b': 2}}, 'a.b', 2),
        ({'a': [1, 2, '3']}, 'a.2', '3'),
        ({'a': {'b': 2}, 'c': []}, 'c', []),
        ({'a': {'b': 2}, 'c': [{'d': {'e': 4}}]}, 'c.0.d.e', 4),
    ])
    def test_pluck(self, data: dict, path: str, expected: Any):
        self.assertEquals(pluck(data, path), expected)

from enum import IntEnum
from typing import Optional, Type
from unittest import TestCase

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

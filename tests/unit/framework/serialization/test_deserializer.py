from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional, Union
from unittest import TestCase

from framework.serialization.deserializer import DictDeserializer
from framework.test.helper import data_provider


class EnumA(IntEnum):
    A = 1
    B = 2
    C = 3


@dataclass
class ClassA:
    a: int = 0
    b: str = ''


@dataclass
class ClassB:
    a: int = 0
    b: str = ''
    c: Optional[int] = None
    d: EnumA = EnumA.A
    e: Optional[EnumA] = None
    f: Optional[ClassA] = ClassA()
    g: List[ClassA] = field(default_factory=list)
    h: Dict[str, ClassA] = field(default_factory=dict)
    i: Union[int, str, ClassA] = 0


class TestDeserializer(TestCase):
    @data_provider([
        (
            {
                'a': 1,
                'b': 'hoge',
                'd': 3,
                'g': [],
                'h': {},
                'i': 1,
            },
            {
                'a': 1,
                'b': 'hoge',
                'c': None,
                'd': EnumA.C,
                'e': None,
                'f': None,
                'g': [],
                'h': {},
                'i': 1,
            },
        ),
        (
            {
                'a': 1,
                'b': 'hoge',
                'c': 2,
                'd': 3,
                'g': [],
                'h': {},
                'i': 'hoge',
            },
            {
                'a': 1,
                'b': 'hoge',
                'c': 2,
                'd': EnumA.C,
                'e': None,
                'f': None,
                'g': [],
                'h': {},
                'i': 'hoge',
            },
        ),
        (
            {
                'a': 1,
                'b': 'hoge',
                'c': 2,
                'd': 3,
                'e': 1,
                'f': {'a': 1, 'b': 'fuga'},
                'g': [{'a': 4, 'b': 'piyo'}],
                'h': {'key': {'a': 5, 'b': 'abcd'}},
                'i': {'a': 6, 'b': 'aaa'},
            },
            {
                'a': 1,
                'b': 'hoge',
                'c': 2,
                'd': EnumA.C,
                'e': EnumA.A,
                'f': ClassA(1, 'fuga'),
                'g': [ClassA(4, 'piyo')],
                'h': {'key': ClassA(5, 'abcd')},
                'i': ClassA(6, 'aaa'),
            },
        ),
    ])
    def test_dict_deserializer(self, data: dict, expected: dict):
        deserializer = DictDeserializer()
        actual = deserializer.deserialize(ClassB, data)
        for key, value in expected.items():
            self.assertEqual(getattr(actual, key), value)

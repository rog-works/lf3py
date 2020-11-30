from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional
from unittest import TestCase

from framework.lang.serialize import DictDeserializer, DictSerializer
from framework.test.helper import data_provider


@dataclass
class DataA:
    a: int = 0
    b: str = ''
    c: bool = False
    d: float = 0.0
    e: dict = field(default_factory=dict)
    f: list = field(default_factory=list)

    @property
    def prop_a(self) -> str:
        return 'prop'

    def method_a(self) -> int:
        return 100


class TestSerialize(TestCase):
    def test_dict_serializer(self):
        data = DataA(10, 'hoge', True, 1.0, {'a': 1}, [1, 2, 3])
        serializer = DictSerializer()
        expected = {
            'a': 10,
            'b': 'hoge',
            'c': True,
            'd': 1.0,
            'e': {'a': 1},
            'f': [1, 2, 3],
        }
        self.assertEqual(serializer.serialize(data), expected)


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


class TestDeserialize(TestCase):
    @data_provider([
        (
            {
                'a': 1,
                'b': 'hoge',
                'd': 3,
                'g': [],
                'h': {},
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
            },
        ),
    ])
    def test_dict_deserializer(self, data: dict, expected: dict):
        deserializer = DictDeserializer()
        actual = deserializer.deserialize(ClassB, data)
        for key, value in expected.items():
            self.assertEqual(getattr(actual, key), value)

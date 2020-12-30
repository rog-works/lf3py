from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Union
from unittest import TestCase

from lf3py.serialization.serializer import DictSerializer


class AbcEnum(Enum):
    A = 'a'
    B = 'b'
    C = 'c'


@dataclass
class DataA:
    a: int = 0
    b: str = ''
    c: bool = False
    d: float = 0.0
    e: Dict[str, int] = field(default_factory=dict)
    f: List[int] = field(default_factory=list)
    g: Union[int, str] = 0
    h: AbcEnum = AbcEnum.A

    @property
    def prop_a(self) -> str:
        return 'prop'

    def method_a(self) -> int:
        return 100


class TestSerializer(TestCase):
    def test_dict_serializer(self):
        data = DataA(10, 'hoge', True, 1.0, {'a': 1}, [1, 2, 3], 'fuga', AbcEnum.C)
        serializer = DictSerializer()
        expected = {
            'a': 10,
            'b': 'hoge',
            'c': True,
            'd': 1.0,
            'e': {'a': 1},
            'f': [1, 2, 3],
            'g': 'fuga',
            'h': 'c',
        }
        self.assertEqual(serializer.serialize(data), expected)

from dataclasses import dataclass, field
from unittest import TestCase

from framework.lang.serialize import DictSerializer


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

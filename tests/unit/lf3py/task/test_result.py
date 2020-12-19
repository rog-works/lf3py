from dataclasses import dataclass
from unittest import TestCase

from lf3py.task.result import Result


@dataclass
class ResultA(Result):
    a: int = 0
    b: str = ''
    _p1: float = 0.0
    __p2: bool = False

    def method_a(self) -> bool:
        return False


class TestDict(TestCase):
    def test_result(self):
        result = ResultA(a=1, b='hoge')
        expected = {'a': 1, 'b': 'hoge'}
        self.assertEqual(result.serialize(), expected)

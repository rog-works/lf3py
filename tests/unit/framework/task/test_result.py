from dataclasses import dataclass
from unittest import TestCase

from framework.task.result import Result


@dataclass
class ResultA(Result):
    a: int = 0
    b: str = ''


class TestDict(TestCase):
    def test_result(self):
        result = ResultA(1, 'hoge')
        expected = {'a': 1, 'b': 'hoge'}
        self.assertEqual(result.serialize(), expected)

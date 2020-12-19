from typing import Any
from unittest import TestCase

from lf3py.lang.dict import pluck
from lf3py.test.helper import data_provider


class TestDict(TestCase):
    @data_provider([
        ({'a': 1}, 'a', 1),
        ({'a': {'b': 2}}, 'a.b', 2),
        ({'a': [1, 2, '3']}, 'a.2', '3'),
        ({'a': {'b': 2}, 'c': []}, 'c', []),
        ({'a': {'b': 2}, 'c': [{'d': {'e': 4}}]}, 'c.0.d.e', 4),
    ])
    def test_pluck(self, data: dict, path: str, expected: Any):
        self.assertEqual(pluck(data, path), expected)

from typing import Any
from unittest import TestCase

from lf3py.lang.sequence import first, last
from lf3py.test.helper import data_provider


class TestSequence(TestCase):
    @data_provider([
        ([1, 2, 3], 1),
        (map(lambda a: a, [1, 2, 3]), 1),
        (filter(lambda a: True, [1, 2, 3]), 1),
        ({'a': 1, 'b': 2, 'c': 3}.values(), 1),
        ({'a': 1, 'b': 2, 'c': 3}.keys(), 'a'),
    ])
    def test_first(self, iter: Any, expected: Any):
        self.assertEqual(expected, first(iter))

    @data_provider([
        ([1, 2, 3], 3),
        (map(lambda a: a, [1, 2, 3]), 3),
        (filter(lambda a: True, [1, 2, 3]), 3),
        ({'a': 1, 'b': 2, 'c': 3}.values(), 3),
        ({'a': 1, 'b': 2, 'c': 3}.keys(), 'c'),
    ])
    def test_last(self, iter: Any, expected: Any):
        self.assertEqual(expected, last(iter))

from unittest import TestCase

from lf2.lang.inspect import default_args


class TestInspect(TestCase):
    def test_default_args(self):
        def default_none(n: int):
            pass

        def default_a(a: int = 0):
            pass

        def default_ab(a: int = 1, b: str = 'hoge'):
            pass

        self.assertEqual(default_args(default_none), {})
        self.assertEqual(default_args(default_a), {'a': 0})
        self.assertEqual(default_args(default_ab), {'a': 1, 'b': 'hoge'})

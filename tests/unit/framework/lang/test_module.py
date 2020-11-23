from unittest import TestCase

from framework.lang.module import load_module


class ClassA:
    pass


def func_a():
    pass


value_a = 1


class TestModule(TestCase):
    def test_load_module(self):
        self.assertEqual(load_module(self.__module__, 'ClassA'), ClassA)
        self.assertEqual(load_module(self.__module__, 'func_a'), func_a)
        self.assertEqual(load_module(self.__module__, 'value_a'), value_a)

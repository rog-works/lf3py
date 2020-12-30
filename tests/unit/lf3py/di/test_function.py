from unittest import TestCase

from lf3py.di import DI
from lf3py.di.invoker import invoke, currying


class SymbolA:
    pass


class SymbolB:
    def __init__(self, a: SymbolA) -> None:
        self.a = a


class SymbolC:
    def __init__(self, b: SymbolB) -> None:
        self.b = b


def injector_c(b: SymbolB) -> SymbolC:
    return SymbolC(b)


class TestFunction(TestCase):
    def test_invoke(self):
        di = DI()
        di.register(SymbolA, SymbolA)
        di.register(SymbolB, SymbolB)
        self.assertEqual(type(invoke(di, injector_c)), SymbolC)

    def test_currying(self):
        di = DI()
        di.register(SymbolA, SymbolA)

        def hoge(fuga: int, a: SymbolA):
            pass

        try:
            curried = currying(di, hoge)
            curried(1)
        except Exception as e:
            self.fail(e)

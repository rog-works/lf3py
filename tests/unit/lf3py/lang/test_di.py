from unittest import TestCase

from lf3py.lang.di import DI


class SymbolA:
    def __init__(self) -> None:
        pass


class SymbolB:
    def __init__(self, a: SymbolA) -> None:
        self.a = a


class SymbolC:
    def __init__(self, b: SymbolB) -> None:
        self.b = b


def injector_c(b: SymbolB) -> SymbolC:
    return SymbolC(b)


def injector_b_default(a: SymbolA = SymbolA()) -> SymbolB:
    return SymbolB(a)


class TestDI(TestCase):
    def test_resolve(self):
        di = DI()
        di.register(SymbolA, SymbolA)
        self.assertEqual(type(di.resolve(SymbolA)), SymbolA)

        di = DI()
        di.register(SymbolA, SymbolA)
        di.register(SymbolB, SymbolB)
        self.assertEqual(type(di.resolve(SymbolB)), SymbolB)
        self.assertEqual(type(di.resolve(SymbolB).a), SymbolA)

        di = DI()
        di.register(SymbolA, SymbolA)
        di.register(SymbolB, SymbolB)
        di.register(SymbolC, SymbolC)
        self.assertEqual(type(di.resolve(SymbolC)), SymbolC)
        self.assertEqual(type(di.resolve(SymbolC).b), SymbolB)
        self.assertEqual(type(di.resolve(SymbolC).b.a), SymbolA)

        di = DI()
        di.register(SymbolA, lambda: SymbolA())
        self.assertEqual(type(di.resolve(SymbolA)), SymbolA)

        di = DI()
        di.register(SymbolA, SymbolA)
        di.register(SymbolB, SymbolB)
        di.register(SymbolC, injector_c)
        self.assertEqual(type(di.resolve(SymbolC)), SymbolC)
        self.assertEqual(type(di.resolve(SymbolC).b), SymbolB)
        self.assertEqual(type(di.resolve(SymbolC).b.a), SymbolA)
        self.assertEqual(type(di.resolve(SymbolC).b.a), SymbolA)

        di = DI()
        di.register(SymbolB, injector_b_default)
        self.assertEqual(type(di.resolve(SymbolB)), SymbolB)
        self.assertEqual(type(di.resolve(SymbolB).a), SymbolA)

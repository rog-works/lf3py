from unittest import TestCase

from lf3py.task.transaction import transaction


def error_func():
    e = False  # noqa: F841
    f = 0.0  # noqa: F841
    raise ValueError()


class TestTransation(TestCase):
    def test_transaction(self):
        try:
            a = 1  # noqa: F841
            b = 'hoge'  # noqa: F841
            self.transaction_func()
        except ValueError:
            pass

    def transaction_func(self):
        with transaction(error_handler=self.error_handler):
            c = True  # noqa: F841
            d = 1.0  # noqa: F841
            error_func()

    def error_handler(self, error: BaseException, context: dict):
        self.assertEqual(type(error), ValueError)
        self.assertEqual(context.get('a'), None)
        self.assertEqual(context.get('b'), None)
        self.assertEqual(context['c'], True)
        self.assertEqual(context['d'], 1.0)
        self.assertEqual(context.get('e'), None)
        self.assertEqual(context.get('f'), None)

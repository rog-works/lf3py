from unittest import TestCase

from lf3py.i18n.translator import Translator
from lf3py.test.helper import data_provider


class TestTranslator(TestCase):
    CONFIG = {
        'http': {
            '500': '500 Internal Server Error',
        },
    }

    @data_provider([
        ('http.500', '500 Internal Server Error'),
    ])
    def test_trans(self, path: str, expected: str):
        translator = Translator(self.CONFIG)
        self.assertEqual(translator.trans(path), expected)

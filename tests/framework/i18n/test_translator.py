from unittest import TestCase

from framework.i18n.translator import Translator
from tests.helper.fixture import data_provider


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

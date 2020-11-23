from datetime import datetime
from unittest import TestCase

from framework.i18n.datetime import DateTime
from framework.i18n.tzinfo import TZInfo
from tests.helper.fixture import data_provider


class TestDateTime(TestCase):
    def test_now(self):
        dt = DateTime(TZInfo('ja'))
        self.assertEquals(type(dt.now()), datetime)

    @data_provider([
        ('%Y-%m-%dT%H:%M:%S.%f%z', r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{4}$'),
    ])
    def test_strftime(self, fmt: str, expected: str):
        dt = DateTime(TZInfo('ja'))
        self.assertRegex(dt.strftime(fmt), expected)

    @data_provider([
        ('2020-11-23 12:00:00', '%Y-%m-%d %H:%M:%S', '2020-11-23 12:00:00'),
    ])
    def test_strptime(self, date: str, format: str, expected: str):
        dt = DateTime(TZInfo('ja'))
        self.assertEquals(dt.strptime(date, format).strftime(format), expected)

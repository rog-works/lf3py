from datetime import datetime
from unittest import TestCase

from lf2.i18n.datetime import DateTime
from lf2.i18n.tzinfo import TZInfo
from lf2.test.helper import data_provider


class TestDateTime(TestCase):
    def test_now(self):
        dt = DateTime(TZInfo(9, 0, 'Asia/Tokyo'))
        self.assertEqual(type(dt.now()), datetime)

    @data_provider([
        ('%Y-%m-%dT%H:%M:%S.%f%z', r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{4}$'),
    ])
    def test_strftime(self, fmt: str, expected: str):
        dt = DateTime(TZInfo(9, 0, 'Asia/Tokyo'))
        self.assertRegex(dt.strftime(fmt), expected)

    @data_provider([
        ('2020-11-23 12:00:00', '%Y-%m-%d %H:%M:%S', '2020-11-23 12:00:00'),
    ])
    def test_strptime(self, date: str, format: str, expected: str):
        dt = DateTime(TZInfo(9, 0, 'Asia/Tokyo'))
        self.assertEqual(dt.strptime(date, format).strftime(format), expected)

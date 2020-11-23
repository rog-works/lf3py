from datetime import timedelta
from unittest import TestCase

from framework.i18n.tzinfo import TZInfo


class TestTZInfo(TestCase):
    def test_tzinfo(self):
        tz = TZInfo('ja')
        self.assertEqual(tz.utcoffset(), timedelta(hours=9))
        self.assertEqual(tz.dst(), timedelta(0))
        self.assertEqual(tz.tzname(), 'Asia/Tokyo')

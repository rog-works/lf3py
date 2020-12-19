from datetime import datetime, timedelta
from unittest import TestCase

from lf3py.i18n.tzinfo import TZInfo


class TestTZInfo(TestCase):
    def test_tzinfo(self):
        tz = TZInfo(9, 0, 'Asia/Tokyo')
        dt = datetime.now
        self.assertEqual(tz.utcoffset(dt), timedelta(hours=9))
        self.assertEqual(tz.dst(dt), timedelta(0))
        self.assertEqual(tz.tzname(dt), 'Asia/Tokyo')

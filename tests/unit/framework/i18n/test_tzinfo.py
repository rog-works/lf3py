from datetime import datetime, timedelta
from unittest import TestCase

from framework.i18n.tzinfo import TZInfo


class TestTZInfo(TestCase):
    def test_tzinfo(self):
        tz = TZInfo('ja')
        dt = datetime.now
        self.assertEqual(tz.utcoffset(dt), timedelta(hours=9))
        self.assertEqual(tz.dst(dt), timedelta(0))
        self.assertEqual(tz.tzname(dt), 'Asia/Tokyo')

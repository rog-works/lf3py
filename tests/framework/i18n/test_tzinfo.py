from datetime import timedelta
from unittest import TestCase

from framework.i18n.tzinfo import TZInfo


class TestTZInfo(TestCase):
    def test_tzinfo(self):
        tz = TZInfo('ja')
        self.assertEquals(tz.utcoffset(), timedelta(hours=9))
        self.assertEquals(tz.dst(), timedelta(0))
        self.assertEquals(tz.tzname(), 'Asia/Tokyo')

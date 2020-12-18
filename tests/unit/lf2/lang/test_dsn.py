from typing import List
from unittest import TestCase

from lf2.lang.dsn import DSN
from lf2.test.helper import data_provider


class TestDSN(TestCase):
    @data_provider([
        (['event', 'on'], 'event.on'),
        (['event', 'off'], 'event.off'),
    ])
    def test_format(self, elems: List[str], expected: str):
        self.assertEqual(DSN.format(*elems), expected)

    @data_provider([
        ('event.on', 'event.(on|off)', True),
        ('event.off', 'event.(on|off)', True),
        ('event.invalid', 'event.(on|off)', False),
    ])
    def test_like(self, dsn: str, spec: str, expected: bool):
        self.assertEqual(DSN(dsn).contains(spec), expected)

    @data_provider([
        ('event.on', 'event.(?P<switch>(on|off))', {'switch': 'on'}),
        ('event.off', 'event.(?P<switch>(on|off))', {'switch': 'off'}),
    ])
    def test_capture(self, dsn: str, spec: str, expected: bool):
        self.assertEqual(DSN(dsn).capture(spec), expected)

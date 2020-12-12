from typing import List
from unittest import TestCase

from lf2.api.path import PathDSN
from lf2.test.helper import data_provider


class TestPathDSN(TestCase):
    @data_provider([
        (['GET', '/models/1234'], 'GET /models/1234'),
        (['GET', '/models/1234/attrs/name'], 'GET /models/1234/attrs/name'),
    ])
    def test_format(self, elems: List[str], expected: bool):
        self.assertEqual(PathDSN.format(*elems), expected)

    @data_provider([
        ('GET /models/1234', 'GET /models/{model_id}', True),
        ('GET /models/1234/attrs/name', 'GET /models/{model_id}/attrs/{attr}', True),
    ])
    def test_like(self, path: str, path_spec: str, expected: bool):
        dsn = PathDSN(path)
        self.assertEqual(dsn.like(path_spec), expected)

    @data_provider([
        (
            'GET /models/1234',
            'GET /models/{model_id}',
            {'model_id': '1234'},
        ),
        (
            'GET /models/1234/attrs/name',
            'GET /models/{model_id}/attrs/{attr}',
            {'model_id': '1234', 'attr': 'name'},
        ),
    ])
    def test_capture(self, path: str, path_spec: str, expected: dict):
        dsn = PathDSN(path)
        self.assertEqual(dsn.capture(path_spec), expected)

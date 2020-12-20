from typing import List
from unittest import TestCase

from lf3py.api.dsn import ApiDSN
from lf3py.test.helper import data_provider


class TestRouteDSN(TestCase):
    @data_provider([
        (['GET', '/models/1234'], 'GET /models/1234'),
        (['GET', '/models/1234/attrs/name'], 'GET /models/1234/attrs/name'),
    ])
    def test_format(self, elems: List[str], expected: bool):
        self.assertEqual(ApiDSN.format(*elems), expected)

    @data_provider([
        ('GET /models/1234', 'GET /models/{model_id}', True),
        ('GET /models/1234/attrs/name', 'GET /models/{model_id}/attrs/{attr}', True),
    ])
    def test_contains(self, path: str, path_spec: str, expected: bool):
        dsn = ApiDSN(path)
        self.assertEqual(dsn.contains(path_spec), expected)

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
        dsn = ApiDSN(path)
        self.assertEqual(dsn.capture(path_spec), expected)

    def test_to_str(self):
        dsn = ApiDSN('GET', '/ping')
        self.assertEqual(str(dsn), 'GET /ping')

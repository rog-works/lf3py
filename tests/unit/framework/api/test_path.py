from unittest import TestCase

from framework.api.path import capture_params
from framework.test.helper import data_provider


class TestPath(TestCase):
    @data_provider([
        (
            '/models/1234',
            '/models/{model_id}',
            {'model_id': '1234'},
        ),
        (
            '/models/1234/attrs/name',
            '/models/{model_id}/attrs/{attr}',
            {'model_id': '1234', 'attr': 'name'},
        ),
    ])
    def test_capture_params(self, path: str, path_spec: str, expected: dict):
        actual = capture_params(path, path_spec)
        self.assertEqual(actual, expected)

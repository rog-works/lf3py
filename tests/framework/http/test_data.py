from unittest import TestCase

from framework.http.data import Response
from tests.helper.fixture import data_provider


class TestData(TestCase):
    @data_provider([
        (
            {
                'status': 200,
                'headers': {'content-type': 'application/json'},
                'body': {'success': True}
            },
        ),
    ])
    def test_response(self, res: dict):
        response = Response(status=res['status'], headers=res['headers'], body=res['body'])
        self.assertEquals(response.serialize(), res)

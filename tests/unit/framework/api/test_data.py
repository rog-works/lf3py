from unittest import TestCase

from framework.api.data import Request, Response
from tests.helper.fixture import data_provider


class TestData(TestCase):
    @data_provider([
        (
            {
                'path': '/models',
                'method': 'GET',
                'headers': {'content-type': 'application/json'},
                'params': {'model_id': 1234}
            },
        ),
    ])
    def test_request(self, req: dict):
        request = Request(path=req['path'], method=req['method'], headers=req['headers'], params=req['params'])
        self.assertEqual(request.path, req['path'])
        self.assertEqual(request.method, req['method'])
        self.assertEqual(request.headers, req['headers'])
        self.assertEqual(request.params, req['params'])

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
        self.assertEqual(response.status, res['status'])
        self.assertEqual(response.headers, res['headers'])
        self.assertEqual(response.body, res['body'])
        self.assertEqual(response.serialize(), res)

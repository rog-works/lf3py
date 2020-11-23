from unittest import TestCase

from framework.http.data import Request, Response
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
        self.assertEquals(request.path, req['path'])
        self.assertEquals(request.method, req['method'])
        self.assertEquals(request.headers, req['headers'])
        self.assertEquals(request.params, req['params'])

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
        self.assertEquals(response.status, res['status'])
        self.assertEquals(response.headers, res['headers'])
        self.assertEquals(response.body, res['body'])
        self.assertEquals(response.serialize(), res)

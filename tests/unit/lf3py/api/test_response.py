from unittest import TestCase

from lf3py.api.response import Response


class TestResponse(TestCase):
    def test_content_type(self):
        response = Response()
        self.assertEqual(response.json().serialize(), {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': {}})
        self.assertEqual(response.html().serialize(), {'statusCode': 200, 'headers': {'Content-Type': 'text/html'}, 'body': {}})
        self.assertEqual(response.text().serialize(), {'statusCode': 200, 'headers': {'Content-Type': 'text/plain'}, 'body': {}})

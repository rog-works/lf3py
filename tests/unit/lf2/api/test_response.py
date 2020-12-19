from unittest import TestCase

from lf2.api.response import Response


class TestResponse(TestCase):
    def test_content_type(self):
        response = Response()
        self.assertEqual(response.json().serialize(), {'status': 200, 'headers': {'Content-Type': 'application/json'}, 'body': {}})
        self.assertEqual(response.html().serialize(), {'status': 200, 'headers': {'Content-Type': 'text/html'}, 'body': {}})
        self.assertEqual(response.text().serialize(), {'status': 200, 'headers': {'Content-Type': 'text/plain'}, 'body': {}})

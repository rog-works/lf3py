import base64
import json
import hmac
from unittest import TestCase

from lf3py.api.errors import UnauthorizedError
from lf3py.api.request import Request
from lf3py.middleware.api.security import jwt, JWTSecret
from lf3py.test.helper import data_provider


class TestJwt(TestCase):
    @data_provider([
        (
            {'alg': 'sha256', 'typ': 'JWT'},
            {'iat': 1516239022, 'sub': '1234'},
            'secret',
        ),
    ])
    def test_jwt(self, head: dict, payload: dict, secret: JWTSecret):
        elems = [
            base64.urlsafe_b64encode(json.dumps(head).encode('utf-8')).decode('utf-8'),
            base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8'),
        ]
        unsigned_token = '.'.join([elem.rstrip('=') for elem in elems])
        sign = hmac.new(secret.encode('utf-8'), unsigned_token.encode('utf-8'), head['alg']).hexdigest()
        jwt_token = f'{unsigned_token}.{sign}'
        request = Request(headers={'Authorization': f'Bearer {jwt_token}'})
        try:
            jwt(request, secret)
        except UnauthorizedError as e:
            self.fail(e)

import base64
import json
import hmac
import re

from lf3py.api.errors import UnauthorizedError
from lf3py.api.request import Request


class JWTSecret(str): pass


def jwt(request: Request, secret: JWTSecret):
    jwt_value = request.headers.get('Authorization', '')
    if not jwt_value:
        raise UnauthorizedError('Not found authorization header')

    sign = ''
    org_sign = ''
    try:
        matches = re.match(r'^Bearer\s+([\w\d]+)\.([\w\d]+)\.([\w\d]+)$', jwt_value)
        enc_head, enc_payload, org_sign = matches.groups()
        head = json.loads(base64.urlsafe_b64decode(enc_head))
        message = f'{enc_head}.{enc_payload}'.encode('utf-8')
        method = hmac.new(secret.encode('utf-8'), message, head['alg'])
        sign = method.hexdigest()
    except Exception as e:
        raise UnauthorizedError(f'Unexpected JWT format. jwt = {jwt_value}') from e

    if org_sign != sign:
        raise UnauthorizedError(f'Not match JWT sign. orginal = {org_sign}, sign = {sign}. jwt = {jwt_value}')

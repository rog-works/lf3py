from unittest import TestCase

from lf2.api.provider import api_router, bp_router, request
from lf2.api.request import Request
from lf2.aws.types import LambdaEvent
from lf2.task.result import Result
from lf2.task.router import Router, Routes


def action_1() -> Result:
    return Result()


def action_2() -> Result:
    return Result()


class TestProvider(TestCase):
    def test_request(self):
        event = LambdaEvent(
            httpMethod='GET',
            path='/',
            headers={},
            queryStringParameters={},
        )
        req = request(event)
        self.assertEqual(type(req), Request)

    def test_bp_router(self):
        router = bp_router(Routes())
        self.assertEqual(type(router), Router)

    def test_ap_router(self):
        router = api_router()
        self.assertEqual(type(router), Router)

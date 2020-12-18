from unittest import TestCase

from lf2.api.provider import api_router, bp_router, request, runner
from lf2.api.request import Request
from lf2.api.route import BpRoute
from lf2.aws.types import LambdaEvent
from lf2.task.result import Result
from lf2.task.router import Router, Routes
from lf2.task.runner import Runner
from lf2.test.helper import data_provider


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

    @data_provider([
        ('GET', '/action/1', action_1),
        ('GET', '/action/2', action_2),
    ])
    def test_runner(self, method: str, path: str, expected: Runner):
        routes = Routes({
            'GET /action/1': f'{__name__}.action_1',
            'GET /action/2': f'{__name__}.action_2',
        })
        router = bp_router(routes)
        event = LambdaEvent(httpMethod=method, path=path, headers={})
        request = Request.from_event(event)
        route = BpRoute(request, router)
        actual = runner(request, route)
        self.assertEqual(actual, expected)

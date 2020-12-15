from unittest import TestCase

from lf2.api.data import Request
from lf2.api.provider import api_router, runner
from lf2.task.result import Result
from lf2.task.router import Router, Routes
from lf2.test.helper import data_provider


def action_1() -> Result:
    return Result()


def action_2() -> Result:
    return Result()


class TestProvider(TestCase):
    def test_api_router(self):
        router = api_router(Routes())
        self.assertEqual(type(router), Router)

    @data_provider([
        ('GET', '/action/1', action_1),
        ('GET', '/action/2', action_2),
    ])
    def test_runner(self, method: str, path: str, expected: dict):
        routes = Routes({
            'GET /action/1': f'{__name__}.action_1',
            'GET /action/2': f'{__name__}.action_2',
        })
        router = api_router(routes)
        actual = runner(Request(method=method, path=path), router)
        self.assertEqual(actual, expected)

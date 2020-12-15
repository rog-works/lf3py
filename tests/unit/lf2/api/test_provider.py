from unittest import TestCase

from lf2.api.data import Request
from lf2.api.provider import api_router, runner
from lf2.task.result import Result
from lf2.task.router import Router, Routes


def action() -> Result:
    return Result()


class TestProvider(TestCase):
    def test_api_router(self):
        router = api_router(Routes())
        self.assertEqual(type(router), Router)

    def test_runner(self):
        routes = Routes({'GET /action': f'{__name__}.action'})
        router = api_router(routes)
        actual = runner(Request(method='GET', path='/action'), router)
        self.assertEqual(actual, action)

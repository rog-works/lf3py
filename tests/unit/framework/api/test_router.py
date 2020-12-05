from unittest import TestCase

from framework.api.router import resolver
from framework.task.result import Result


def runner_a() -> Result:
    return Result()


def runner_b() -> Result:
    return Result()


class TestRouter(TestCase):
    def test_resolve(self):
        routes = {
            'GET /models': runner_a,
            r'GET /models/\d+': runner_b,
        }
        self.assertEqual(resolver(routes, 'GET', '/models'), runner_a)
        self.assertEqual(resolver(routes, 'GET', '/models/1234'), runner_b)

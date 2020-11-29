from unittest import TestCase

from framework.api.router import Router
from framework.task.result import Result


def runner_a() -> Result:
    return Result()


def runner_b() -> Result:
    return Result()


class TestRouter(TestCase):
    def test_resolve(self):
        router = Router({
            'GET /models': runner_a,
            r'GET /models/\d+': runner_b,
        })
        self.assertEqual(router.resolve('GET', '/models'), runner_a)
        self.assertEqual(router.resolve('GET', '/models/1234'), runner_b)

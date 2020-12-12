from unittest import TestCase

from framework.lang.dsn import DSN
from framework.task.router import Router
from framework.task.result import Result
from framework.task.runner import Runner
from framework.test.helper import data_provider


def runner_a() -> Result:
    return Result()


def runner_b() -> Result:
    return Result()


class TestRouter(TestCase):
    @data_provider([
        ('GET /models', runner_a, 'GET /models'),
        ('GET /models/\\d+', runner_b, 'GET /models/1234'),
    ])
    def test_resolve(self, spec: str, runner: Runner, dsn: str):
        router = Router(DSN)
        router.register(runner, spec)
        actual = router.resolve(dsn)
        self.assertEqual(f'{actual.__module__}.{actual.__name__}', f'{runner.__module__}.{runner.__name__}')

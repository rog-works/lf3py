from unittest import TestCase

from lf3py.lang.dsn import DSN
from lf3py.routing.routers import Router
from lf3py.task.data import Result
from lf3py.task.types import Runner
from lf3py.test.helper import data_provider


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
        _, module_path = router.resolve(dsn)
        self.assertEqual(module_path, f'{runner.__module__}.{runner.__name__}')

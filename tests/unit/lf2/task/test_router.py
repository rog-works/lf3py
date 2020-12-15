from unittest import TestCase

from lf2.lang.dsn import DSN
from lf2.task.router import Router
from lf2.task.result import Result
from lf2.task.runner import Runner
from lf2.test.helper import data_provider


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

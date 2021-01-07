from unittest import TestCase

from lf3py.config.types import Routes
from lf3py.lang.dsn import DSN
from lf3py.routing.router import BpRouter, InlineRouter
from lf3py.routing.types import RunnerMiddleware
from lf3py.task.data import Result
from lf3py.test.helper import data_provider


def runner_a() -> Result:
    return Result()


def runner_b() -> Result:
    return Result()


class TestInlineRouter(TestCase):
    @data_provider([
        ('GET /models', runner_a, 'GET /models'),
        ('GET /models/\\d+', runner_b, 'GET /models/1234'),
    ])
    def test_resolve(self, spec: str, runner: RunnerMiddleware, dsn: str):
        router = InlineRouter(DSN)
        router.register(spec, runner)
        _, actual = router.resolve(dsn)
        self.assertEqual([runner], actual)

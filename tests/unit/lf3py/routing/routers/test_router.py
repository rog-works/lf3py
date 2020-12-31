from unittest import TestCase

from lf3py.config.types import Routes
from lf3py.lang.dsn import DSN
from lf3py.routing.router import BpRouter, FlowRouter
from lf3py.task.data import Result
from lf3py.task.types import Runner
from lf3py.test.helper import data_provider


def runner_a() -> Result:
    return Result()


def runner_b() -> Result:
    return Result()


class TestBpRouter(TestCase):
    @data_provider([
        ('GET /models', runner_a),
        ('GET /models/1234', runner_b),
    ])
    def test_resolve(self, dsn: str, expected: Runner):
        routes = Routes({
            'GET /models': f'{runner_a.__module__}.{runner_a.__name__}',
            'GET /models/\\d+': f'{runner_b.__module__}.{runner_b.__name__}',
        })
        router = BpRouter(DSN, routes)
        _, actual = router.resolve(dsn)
        self.assertEqual(expected, actual)


class TestFlowRouter(TestCase):
    @data_provider([
        ('GET /models', runner_a, 'GET /models'),
        ('GET /models/\\d+', runner_b, 'GET /models/1234'),
    ])
    def test_resolve(self, spec: str, runner: Runner, dsn: str):
        router = FlowRouter(DSN)
        router.register(runner, spec)
        _, actual = router.resolve(dsn)
        self.assertEqual(runner, actual)

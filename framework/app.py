from logging import Logger
from typing import Dict

from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.lang.di import DI
from framework.plugins.api import Api
from framework.task.result import Result
from framework.task.runner import Runner


class App:
    __instances: Dict[str, 'App'] = {}

    @classmethod
    def get(cls, name: str) -> 'App':
        return cls.__instances[name]

    def __init__(self, name: str, di: DI) -> None:
        self._name = name
        self._di = di
        self.__instances[name] = self

    @property
    def config(self) -> dict:
        return self._di.resolve(Config)

    @property
    def i18n(self) -> I18n:
        return self._di.resolve(I18n)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def api(self) -> Api:
        return self._di.resolve(Api)

    def run(self) -> Result:
        runner: Runner = self._di.resolve(Runner)
        return runner()

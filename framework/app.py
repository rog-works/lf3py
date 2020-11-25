from logging import Logger
from typing import Optional

from framework.api.api import Api
from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.lang.di import DI
from framework.task.result import Result
from framework.task.runner import Runner


class App:
    __instance: Optional['App'] = None

    @classmethod
    def get(cls) -> 'App':
        if cls.__instance is None:
            raise ModuleNotFoundError()

        return cls.__instance

    def __init__(self, di: DI) -> None:
        self._di = di
        App.__instance = self

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

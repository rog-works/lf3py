from logging import Logger
from typing import Optional

from framework.api.api import Api
from framework.app import App as BaseApp
from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.lang.cache import Cache
from framework.lang.di import DI


class App(BaseApp):
    __instance: Optional['App'] = None

    @classmethod
    def get(cls) -> 'App':
        if cls.__instance is None:
            raise AssertionError()

        return cls.__instance

    @classmethod
    def create(cls, di: DI) -> 'App':
        cls.__instance = cls(di)
        return cls.__instance

    @property
    def config(self) -> Config:
        return self._di.resolve(Config)

    @property
    def i18n(self) -> I18n:
        return self._di.resolve(I18n)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def cache(self) -> Cache:
        return self._di.resolve(Cache)

    @property
    def api(self) -> Api:
        return self._di.resolve(Api)

from logging import Logger
from typing import Optional

from lf3py.app.apiapp import ApiApp
from lf3py.cache import Cache
from lf3py.i18n import I18n
from lf3py.lang.di import DI


class MyApp(ApiApp):
    __instance: Optional['MyApp'] = None

    @classmethod
    def instance(cls) -> 'MyApp':
        if cls.__instance is None:
            raise AssertionError()

        return cls.__instance

    def __init__(self, di: DI) -> None:
        super(MyApp, self).__init__(di)
        MyApp.__instance = self

    @property
    def i18n(self) -> I18n:
        return self._di.resolve(I18n)

    @property
    def logger(self) -> Logger:
        return self._di.resolve(Logger)

    @property
    def cache(self) -> Cache:
        return self._di.resolve(Cache)

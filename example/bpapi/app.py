from logging import Logger

from lf3py.app.apiapp import ApiApp
from lf3py.cache import Cache
from lf3py.config import ModuleDefinitions
from lf3py.i18n import I18n

from example.bpapi.config.modules import modules


class MyApp(ApiApp):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return modules()

    @property
    def i18n(self) -> I18n:
        return self._locator.resolve(I18n)

    @property
    def logger(self) -> Logger:
        return self._locator.resolve(Logger)

    @property
    def cache(self) -> Cache:
        return self._locator.resolve(Cache)

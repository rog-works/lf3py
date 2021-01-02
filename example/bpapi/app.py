from logging import Logger

from lf3py.app.apiapp import ApiApp
from lf3py.app.definitions import bpapi_modules
from lf3py.cache import Cache
from lf3py.config import ModuleDefinitions
from lf3py.i18n import I18n

from example.bpapi.config.modules import add_modules


class MyApp(ApiApp):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return {**bpapi_modules(), **add_modules()}

    @property
    def i18n(self) -> I18n:
        return self.locate(I18n)

    @property
    def logger(self) -> Logger:
        return self.locate(Logger)

    @property
    def cache(self) -> Cache:
        return self.locate(Cache)

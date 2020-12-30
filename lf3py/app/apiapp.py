from lf3py.api.errors.handler import ApiErrorHandler
from lf3py.api.router import IApiRouter
from lf3py.api.symbols import IApiRender
from lf3py.app.app import App
from lf3py.app.definitions import flowapi_modules
from lf3py.config import ModuleDefinitions
from lf3py.di.function import invoke
from lf3py.routing.dispatcher import dispatch
from lf3py.task.data import Result


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return flowapi_modules()

    @property
    def render(self) -> IApiRender:
        return self._locator.resolve(IApiRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._locator.resolve(ApiErrorHandler)

    @property
    def api(self) -> IApiRouter:
        return self._locator.resolve(IApiRouter)

    def run(self) -> Result:
        return invoke(self.locator, dispatch)

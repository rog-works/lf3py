from lf3py.api.errors.handler import ApiErrorHandler
from lf3py.api.render import ApiRender
from lf3py.api.request import Request
from lf3py.api.router import IApiRouter
from lf3py.app.app import App
from lf3py.app.definitions import flowapi_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.task.data import Result


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return flowapi_modules()

    @property
    def render(self) -> ApiRender:
        return self._locator.resolve(ApiRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._locator.resolve(ApiErrorHandler)

    @property
    def api(self) -> IApiRouter:
        return self._locator.resolve(IApiRouter)

    def run(self) -> Result:
        with self.start():
            return self.api.dispatch(self._locator.resolve(Request))

    @hook
    def entry(self, event: dict, context: object):
        self._locator.register(LambdaEvent, lambda: event)

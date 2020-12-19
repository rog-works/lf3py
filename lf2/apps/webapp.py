from lf2.api.errors.handler import ApiErrorHandler
from lf2.api.render import ApiRender
from lf2.api.request import Request
from lf2.api.route import Route
from lf2.apps.app import App
from lf2.apps.definitions import webapi_modules
from lf2.aws.hooks.method import hook
from lf2.aws.types import LambdaEvent
from lf2.task.result import Result


class WebApp(App):
    @classmethod
    def default_modules(cls) -> dict:
        return webapi_modules()

    @property
    def route(self) -> Route:
        return self._di.resolve(Route)

    @property
    def render(self) -> ApiRender:
        return self._di.resolve(ApiRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._di.resolve(ApiErrorHandler)

    def run(self) -> Result:
        return self.route.dispatch(self._di.resolve(Request))

    @hook
    def webapi(self, event: dict, context: object):
        self._di.register(LambdaEvent, lambda: event)

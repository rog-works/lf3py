from lf3py.api.errors.handler import ApiErrorHandler
from lf3py.api.render import ApiRender
from lf3py.api.request import Request
from lf3py.api.routers.api import IApiRouter
from lf3py.app.app import App
from lf3py.app.definitions import webapp_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.types import LambdaEvent
from lf3py.task.result import Result


class WebApp(App):
    @classmethod
    def default_modules(cls) -> dict:
        return webapp_modules()

    @property
    def route(self) -> IApiRouter:
        return self._di.resolve(IApiRouter)

    @property
    def render(self) -> ApiRender:
        return self._di.resolve(ApiRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._di.resolve(ApiErrorHandler)

    def run(self) -> Result:
        return self.route.dispatch(self._di.resolve(Request))

    @hook
    def entry(self, event: dict, context: object):
        self._di.register(LambdaEvent, lambda: event)

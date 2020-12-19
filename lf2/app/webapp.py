from lf2.api.errors.handler import ApiErrorHandler
from lf2.api.request import Request
from lf2.api.routers.api import IApiRouter
from lf2.app.app import App
from lf2.app.definitions import webapp_modules
from lf2.aws.hooks.method import hook
from lf2.aws.types import LambdaEvent
from lf2.task.result import Result
from lf2.view.render import IRender


class WebApp(App):
    @classmethod
    def default_modules(cls) -> dict:
        return webapp_modules()

    @property
    def route(self) -> IApiRouter:
        return self._di.resolve(IApiRouter)

    @property
    def render(self) -> IRender:
        return self._di.resolve(IRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._di.resolve(ApiErrorHandler)

    def run(self) -> Result:
        return self.route.dispatch(self._di.resolve(Request))

    @hook
    def entry(self, event: dict, context: object):
        self._di.register(LambdaEvent, lambda: event)

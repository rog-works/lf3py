from lf3py.api.errors.handler import ApiErrorHandler
from lf3py.api.render import ApiRender
from lf3py.api.request import Request
from lf3py.api.router import IApiRouter
from lf3py.app.app import App
from lf3py.app.definitions import flowapi_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.session.session import Session
from lf3py.session.locator import Locatorify
from lf3py.task.data import Result


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return flowapi_modules()

    @property
    def render(self) -> ApiRender:
        return self._di.resolve(ApiRender)

    @property
    def error(self) -> ApiErrorHandler:
        return self._di.resolve(ApiErrorHandler)

    @property
    def api(self) -> IApiRouter:
        return self._di.resolve(IApiRouter)

    def run(self) -> Result:
        with self._di.resolve(Session):
            return self.api.dispatch(self._di.resolve(Request))

    @hook
    def entry(self, event: dict, context: object):
        self._di.register(Session, lambda: Session.push(Locatorify(self._di.resolve)))
        self._di.register(LambdaEvent, lambda: event)

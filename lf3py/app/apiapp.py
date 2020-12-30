from lf3py.api.router import IApiRouter
from lf3py.api.symbols import IApiRender
from lf3py.app.app import App
from lf3py.app.definitions import flowapi_modules
from lf3py.config import ModuleDefinitions
from lf3py.routing.symbols import IDispatcher
from lf3py.task.data import Command, Result


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return flowapi_modules()

    @property
    def render(self) -> IApiRender:
        return self._locator.resolve(IApiRender)

    @property
    def api(self) -> IApiRouter:
        return self._locator.resolve(IApiRouter)

    @property
    def dispatcher(self) -> IDispatcher:
        return self._locator.resolve(IDispatcher)

    def run(self) -> Result:
        return self.dispatcher.dispatch(self._locator.resolve(Command), self.api)

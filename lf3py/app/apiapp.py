from lf3py.api.router import IApiRouter
from lf3py.api.symbols import IApiRender
from lf3py.app.app import App
from lf3py.app.definitions import inlineapi_modules
from lf3py.config import ModuleDefinitions
from lf3py.task.data import Command, Result


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return inlineapi_modules()

    @property
    def render(self) -> IApiRender:
        return self._locator.resolve(IApiRender)

    @property
    def api(self) -> IApiRouter:
        return self._locator.resolve(IApiRouter)

    def run(self) -> Result:
        command = self._locator.resolve(Command)
        with self.middleware.attach(self._locator, self.api, command):
            return self.api.dispatch(command)

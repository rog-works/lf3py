from lf3py.api.router import IApiRouter
from lf3py.api.symbols import IApiRender
from lf3py.app.app import App
from lf3py.app.definitions import inlineapi_modules
from lf3py.config import ModuleDefinitions


class ApiApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return inlineapi_modules()

    @property
    def render(self) -> IApiRender:
        return self.locate(IApiRender)

    @property
    def api(self) -> IApiRouter:
        return self.locate(IApiRouter)

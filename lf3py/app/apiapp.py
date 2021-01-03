from lf3py.api import Api
from lf3py.api.symbols import IApiRender
from lf3py.app.app import App
from lf3py.app.definitions import inlineapi_modules
from lf3py.app.types import IApiBlueprinter
from lf3py.config import ModuleDefinitions


class ApiApp(App):
    @classmethod
    def blueprint(cls) -> IApiBlueprinter:
        return cls()

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return inlineapi_modules()

    @property
    def render(self) -> IApiRender:
        return self.locate(IApiRender)

    @property
    def api(self) -> Api:
        return self.locate(Api)

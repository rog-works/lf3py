from lf3py.api.symbols import IApiRender, IApiRouter, IApiSchema
from lf3py.app.app import App
from lf3py.app.definitions import inlineapi_modules
from lf3py.app.types import ApiBlueprint
from lf3py.config import ModuleDefinitions


class ApiApp(App):
    @classmethod
    def blueprint(cls) -> ApiBlueprint:
        return cls()

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return inlineapi_modules()

    @property
    def render(self) -> IApiRender:
        return self.locate(IApiRender)

    @property
    def api(self) -> IApiRouter:
        return self.locate(IApiRouter)

    @property
    def schema(self) -> IApiSchema:
        return self.locate(IApiSchema)

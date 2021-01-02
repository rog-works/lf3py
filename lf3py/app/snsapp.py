from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.config import ModuleDefinitions
from lf3py.routing.symbols import IRouter


class SNSApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return sns_modules()

    @property
    def route(self) -> IRouter:
        return self.locate(IRouter)

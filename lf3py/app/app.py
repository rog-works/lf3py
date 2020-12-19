from lf3py.app.types import ModuleDefinitions
from lf3py.lang.di import DI


class App:
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self, di: DI) -> None:
        self._di = di

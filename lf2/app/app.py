from lf2.lang.di import DI


class App:
    def __init__(self, di: DI) -> None:
        self._di = di

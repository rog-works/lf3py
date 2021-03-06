import threading
from types import TracebackType
from typing import Dict, Optional, Type

from lf3py.lang.locator import Locator, T_INST


class Session:
    __sessions: Dict[int, 'Session'] = {}

    @classmethod
    def thread_id(cls) -> int:
        return threading.get_ident()

    @classmethod
    def current(cls) -> 'Session':
        return cls.__sessions[cls.thread_id()]

    @classmethod
    def start(cls, locator: Locator) -> 'Session':
        session = cls(locator)
        cls.__sessions[cls.thread_id()] = session
        return session

    def __init__(self, locator: Locator) -> None:
        self._locator = locator

    def __enter__(self) -> 'Session':
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[BaseException], exc_traceback: TracebackType):
        self.close()

    def __call__(self, symbol: Type[T_INST]) -> T_INST:
        return self.resolve(symbol)

    def close(self):
        del self.__sessions[self.thread_id()]

    def can_resolve(self, symbol: Type) -> bool:
        return self._locator.can_resolve(symbol)

    def resolve(self, symbol: Type[T_INST]) -> T_INST:
        return self._locator.resolve(symbol)


def context(symbol: Type[T_INST]) -> T_INST:
    return Session.current()(symbol)

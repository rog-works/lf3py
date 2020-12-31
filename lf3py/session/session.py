import threading
from types import TracebackType
from typing import Dict, Optional, Type, TypeVar

from lf3py.lang.locator import Locator

_T = TypeVar('_T')


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
        del self.__sessions[self.thread_id()]

    def __call__(self, symbol: Type[_T]) -> _T:
        return self.resolve(symbol)

    def can_resolve(self, symbol: Type) -> bool:
        return self._locator.can_resolve(symbol)

    def resolve(self, symbol: Type[_T]) -> _T:
        return self._locator.resolve(symbol)


def context(symbol: Type[_T]) -> _T:
    return Session.current()(symbol)

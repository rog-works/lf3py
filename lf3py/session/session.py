import threading
from typing import Dict, Type, TypeVar

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

    def __enter__(self):
        pass

    def __exit__(self):
        del self.__sessions[self.thread_id()]


def session(symbol: Type[_T]) -> _T:
    return Session.current()._locator.resolve(symbol)

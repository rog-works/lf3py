from types import TracebackType
from typing import List, Optional, Type

from lf3py.locator.types import ILocator


class Session:
    __sessions: List['Session'] = []

    @classmethod
    def current(cls) -> 'Session':
        return cls.__sessions[-1]

    @classmethod
    def push(cls, locator: ILocator) -> 'Session':
        peek = Session(locator)
        cls.__sessions.append(peek)
        return peek

    def __init__(self, locator: ILocator) -> None:
        self._locator = locator

    @property
    def locator(self) -> ILocator:
        return self._locator

    def close(self):
        self.__sessions.pop()

    def __enter__(self):
        self

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[BaseException], exc_traceback: TracebackType):
        self.close()

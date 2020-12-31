from logging import Logger

from lf3py.api.symbols import IApiRender
from lf3py.session import context


class Session:
    @property
    def logger(self) -> Logger:
        return context(Logger)

    @property
    def render(self) -> IApiRender:
        return context(IApiRender)

from typing import Callable, Type

from lf3py.lang.dsn import DSN
from lf3py.task.result import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]
DSNType = Type[DSN]

from typing import Callable

from lf3py.task.data import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]

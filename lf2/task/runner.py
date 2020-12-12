from typing import Callable

from lf2.task.result import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]

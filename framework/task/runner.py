from typing import Callable

from framework.task.result import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]

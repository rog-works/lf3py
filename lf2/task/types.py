from typing import Callable, Dict, Type

from lf2.lang.dsn import DSN
from lf2.task.result import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]
DSNType = Type[DSN]


class Routes(Dict[str, str]): pass

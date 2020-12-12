from typing import Callable, Type, Tuple

from lf2.task.result import Result

ErrorDefinition = Tuple[int, str, Tuple[Type[Exception], ...]]
ErrorHandler = Callable[[int, str, Exception], Result]

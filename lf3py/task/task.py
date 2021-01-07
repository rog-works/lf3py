from dataclasses import dataclass
from typing import Callable, Union

from lf3py.task.data import Result


@dataclass
class Task:
    _run: Callable[[], Union[Result, None]]

    def __call__(self) -> Union[Result, None]:
        return self._run()


@dataclass
class Catch:
    _run: Callable[[Exception], None]

    def __call__(self, error: Exception) -> None:
        return self._run(error)

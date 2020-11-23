from abc import ABCMeta, abstractmethod
from typing import Callable

from framework.task.result import Result


Runner = Callable[..., Result]

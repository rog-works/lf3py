from dataclasses import dataclass
from typing import Callable, List

from lf3py.task.data import Result
from lf3py.task.types import Runner


@dataclass
class Task:
    runner: Runner
    run: Callable[[], Result]


class TaskQueue:
    def __init__(self) -> None:
        self._queue: List[Task] = []

    @property
    def has_next(self) -> bool:
        return len(self._queue) > 0

    def enqueue(self, *tasks: Task):
        self._queue.extend(tasks)

    def __iter__(self) -> 'TaskQueue':
        return self

    def __next__(self) -> Task:
        if not self.has_next:
            raise StopIteration()

        task = self._queue[0]
        self._queue = self._queue[1:]
        return task

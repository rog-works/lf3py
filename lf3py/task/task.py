from abc import ABCMeta
from dataclasses import dataclass
from typing import List, Tuple

from lf3py.task.data import Command, Result
from lf3py.task.types import Runner
from lf3py.routing.invoker import invoke


class IRunnerResolver(metaclass=ABCMeta):
    def resolve(self, dsn: str) -> Tuple[str, Runner]:
        raise NotImplementedError()


@dataclass
class TaskDef:
    command: Command


@dataclass
class Task:
    runner: Runner
    command: Command
    dsn_spec: str

    def run(self) -> Result:
        return invoke(self.runner, self.command, self.dsn_spec)


class TaskQueue:
    def __init__(self, resolver: IRunnerResolver) -> None:
        self._queue: List[Task] = []
        self._resolver = resolver

    @property
    def has_next(self) -> bool:
        return len(self._queue) > 0

    def enqueue(self, task_def: TaskDef):
        self._queue.append(self.__build_task(task_def))

    def __build_task(self, task_def: TaskDef) -> Task:
        dsn_spec, runner = self._resolver.resolve(task_def.command.dsn.to_str())
        return Task(runner, task_def.command, dsn_spec)

    def __iter__(self) -> 'TaskQueue':
        return self

    def __next__(self) -> Task:
        if not self.has_next:
            raise StopIteration()

        task = self._queue[0]
        self._queue = self._queue[1:]
        return task

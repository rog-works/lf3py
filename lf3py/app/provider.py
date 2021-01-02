from lf3py.aws.sns.record import SNSRecords
from lf3py.config import ModuleDefinitions
from lf3py.di import DI
from lf3py.routing.symbols import IRouter
from lf3py.lang.module import load_module_path
from lf3py.task import TaskQueue
from lf3py.task.data import Command


def di_container(modules: ModuleDefinitions) -> DI:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        di.register(
            load_module_path(symbol_module_path),
            load_module_path(inject_module_path)
        )

    return di


def single_task_queue(router: IRouter, command: Command) -> TaskQueue:
    queue = TaskQueue()
    queue.enqueue(router.dispatch(command))
    return queue


def sns_task_queue(router: IRouter, records: SNSRecords) -> TaskQueue:
    queue = TaskQueue()
    queue.enqueue(*[router.dispatch(record) for record in records])
    return queue

from lf3py.aws.sns.record import SNSRecords
from lf3py.config import ModuleDefinitions
from lf3py.di import DI
from lf3py.lang.module import load_module_path
from lf3py.task.data import Command, CommandQueue


def di_container(modules: ModuleDefinitions) -> DI:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        di.register(
            load_module_path(symbol_module_path),
            load_module_path(inject_module_path)
        )

    return di


def single_command_queue(command: Command) -> CommandQueue:
    queue = CommandQueue()
    queue.enqueue(command)
    return queue


def sns_command_queue(records: SNSRecords) -> CommandQueue:
    queue = CommandQueue()
    queue.enqueue(*records)
    return queue

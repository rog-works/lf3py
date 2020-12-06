from framework.api.data import ErrorBody, MessageBody, Result
from framework.lang.error import stacktrace

from example.app import App


def dev_handler(status: int, message: str, error: Exception) -> Result:
    stack_message = stacktrace(error)
    App.get().logger.error(stack_message)
    return ErrorBody(message=message, stacktrace=stack_message)


def prd_handler(status: int, message: str, error: Exception) -> Result:
    stack_message = stacktrace(error)
    App.get().logger.error(stack_message)
    return MessageBody(message=message)

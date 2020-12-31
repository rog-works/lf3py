from types import TracebackType
from typing import Callable, Optional, Type

ErrorHandler = Callable[[BaseException, dict], None]


class Transaction:
    def __init__(self, error_handler: ErrorHandler) -> None:
        self._error_handler = error_handler

    def __enter__(self) -> 'Transaction':
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[BaseException], exc_traceback: TracebackType):
        if exc_value is not None:
            self._error_handler(exc_value, exc_traceback.tb_frame.f_locals)


def transaction(error_handler: ErrorHandler) -> Transaction:
    """
    Examples:
        >>> def action() -> Result:
        >>>     with transaction(error_handler=rollback):
        >>>         publish_id = Model.create()
        >>>         raise ValueError()

        >>> def rollback(error: BaseException, context: dict):
        >>>     print(error)
        >>>     print(context)
        ValueError
        {'publish_id': 100}
    """
    return Transaction(error_handler=error_handler)

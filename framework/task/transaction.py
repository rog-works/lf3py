from typing import Callable, Optional, TracebackType, Type


class Transaction:
    def __init__(self, error_handler: Callable[[Exception, dict], None]) -> None:
        self._error_handler = error_handler

    def __enter__(self) -> 'Transaction':
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[Exception], exc_traceback: TracebackType):
        if exc_value is not None:
            self._error_handler(exc_value, exc_traceback.tb_frame.f_locals)

from typing import Callable, NoReturn

PerformMiddleware = Callable[..., None]
ErrorMiddleware = Callable[[Exception], NoReturn]

from typing import Callable, NoReturn, Optional, Type, Tuple, Union

DIRegister = Tuple[Type, Callable]
Middleware = Callable[..., Union[NoReturn, Optional[DIRegister]]]
ErrorMiddleware = Callable[[Exception], NoReturn]
ErrorMiddlewares = Tuple[ErrorMiddleware, ...]

from typing import Any, Dict, Callable

LambdaHandler = Callable[[dict, object], Dict[str, Any]]
LambdaHandlerDecorator = Callable[[LambdaHandler], LambdaHandler]


class LambdaEvent(dict): pass

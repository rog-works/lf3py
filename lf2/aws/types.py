from typing import Callable

LambdaHandler = Callable[[dict, object], dict]
LambdaHandlerDecorator = Callable[[LambdaHandler], LambdaHandler]


class LambdaEvent(dict): pass

from example.provider import aws_app
from framework.task.result import Result
from framework.lang.module import unload_module


def perform_api(event: dict) -> Result:
    app = aws_app(event, object())
    result = app.run().serialize()
    unload_module(app.runner.__module__)
    return result

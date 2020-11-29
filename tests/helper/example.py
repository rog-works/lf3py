from example.provider import aws_app
from example.router import routes
from framework.api.router import Router
from framework.lang.module import unload_module


def perform_api(event: dict) -> dict:
    app = aws_app(event, object())
    result = app.run().serialize()
    module_path, _ = Router(routes).resolve(app.api.request.method, app.api.request.path)
    unload_module(module_path)
    return result

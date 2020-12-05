from framework.api.router import resolver
from framework.lang.module import unload_module
from framework.task.runner import Runner

from example.config.routes import routes
from example.provider.app import aws_app


def perform_api(event: dict) -> dict:
    app = aws_app(event, object())
    result = app.perform(Runner).serialize()
    module_path, _ = resolver(routes(), app.api.request.method, app.api.request.path)
    unload_module(module_path)
    return result

from framework.api.router import resolver
from framework.lang.module import unload_module
from framework.provider import app_provider

from example.app import App
from example.config.routes import routes
from example.config.modules import modules


def perform_api(event: dict) -> dict:
    app = app_provider(App, modules())
    handler = app.webapi(lambda event, _: app.run().serialize())
    result = handler(event, object())
    module_path, _ = resolver(routes(), app.api.request.method, app.api.request.path)
    unload_module(module_path)
    return result

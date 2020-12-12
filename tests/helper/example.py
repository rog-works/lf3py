from framework.api.path import PathDSN
from framework.lang.module import unload_module
from framework.provider import app_provider
from framework.task.router import Router, Routes

from example.app import App
from example.config.routes import routes
from example.config.modules import modules


def perform_api(event: dict) -> dict:
    app = app_provider(App, modules())
    handler = app.webapi(lambda event, _: app.run().serialize())
    result = handler(event, object())
    router = Router(PathDSN, Routes(routes()))
    module_path = router.resolve_module_path(app.api.request.method, app.api.request.path)
    unload_path = '.'.join(module_path.split('.')[:-1])
    unload_module(unload_path)
    return result

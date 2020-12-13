from lf2.api.path import PathDSN
from lf2.lang.module import unload_module
from lf2.provider import app_provider
from lf2.task.router import Router, Routes

from example.webapi.app import App
from example.webapi.config.routes import routes
from example.webapi.config.modules import modules


def perform_api(event: dict) -> dict:
    app = app_provider(App, modules())
    handler = app.webapi(lambda event, _: app.run().serialize())
    result = handler(event, object())
    router = Router(PathDSN, Routes(routes()))
    module_path = router.resolve_module_path(event['httpMethod'], event['path'])
    unload_path = '.'.join(module_path.split('.')[:-1])
    unload_module(unload_path)
    return result

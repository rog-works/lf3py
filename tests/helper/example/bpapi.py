from lf3py.api.routers.dsn import RouteDSN
from lf3py.app.provider import app_provider
from lf3py.lang.module import unload_module
from lf3py.task.router import Router, Routes

from example.bpapi.app import MyApp
from example.bpapi.config.routes import routes
from example.bpapi.config.modules import modules


def perform_api(event: dict) -> dict:
    app = app_provider(MyApp, modules())
    handler = app.entry(lambda event, _: app.run().serialize())
    result = handler(event, object())
    router = Router(RouteDSN, Routes(routes()))
    _, module_path = router.resolve(event['httpMethod'], event['path'])
    unload_path = '.'.join(module_path.split('.')[:-1])
    unload_module(unload_path)
    return result

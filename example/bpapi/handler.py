import example.bpapi.preprocess  # noqa: F401

from lf3py.app.provider import app_provider
from lf3py.middleware.api.error import route_mismatch, within

from example.bpapi.app import MyApp
from example.bpapi.config.modules import modules

app = app_provider(MyApp, modules())


@app.entry
@app.behavior(route_mismatch, error=within(404))
def handler(event: dict, context: object) -> dict:
    try:
        return app.run().serialize()
    except Exception as e:
        return app.render.fail(e).json().serialize()

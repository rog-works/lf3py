import example.bpapi.preprocess  # noqa: F401

from lf2.app.provider import app_provider

from example.bpapi.app import MyApp
from example.bpapi.config.modules import modules

app = app_provider(MyApp, modules())


@app.entry
def handler(event: dict, context: object) -> dict:
    try:
        return app.run().serialize()
    except Exception as e:
        return app.render.fail(e).json().serialize()

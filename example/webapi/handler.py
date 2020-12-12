import example.webapi.preprocess  # noqa: F401

from lf2.provider import app_provider

from example.webapi.app import App
from example.webapi.config.modules import modules

app = app_provider(App, modules=modules())


@app.webapi
def handler(event: dict, context: object) -> dict:
    try:
        return app.run().serialize()
    except Exception as e:
        return app.api.error_500(e).serialize()

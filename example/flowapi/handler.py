from lf3py.api.response import Response
from lf3py.app.apiapp import ApiApp
from lf3py.app.provider import app_provider

from example.flowapi.model_defs import IndexBody, Model, ShowBody

app = app_provider(ApiApp)


@app.entry
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@app.route('GET', '/models')
def index() -> Response:
    body = IndexBody(models=[Model(id=1234)])
    return app.render.ok(body=body).json()


@app.route('GET', '/models/{model_id}')
def show(model_id: int) -> Response:
    body = ShowBody(model=Model(model_id))
    return app.render.ok(body=body).json()

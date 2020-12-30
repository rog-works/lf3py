from lf3py.api.response import Response
from lf3py.app.apiapp import ApiApp
from lf3py.middleware.api.error import unexpected_dispach, within

from example.flowapi.model_defs import IndexBody, Model, ShowBody

app = ApiApp.blueprint(__name__)


def handler(event: dict, context: object) -> dict:
    return ApiApp.entry(event).run().serialize()


@app.api.get('/models')
def index() -> Response:
    body = IndexBody(models=[Model(id=1234)])
    return app.render.ok(body=body).json()


@app.on_error(*(unexpected_dispach, *within(400)))
@app.api.get('/models/{model_id}')
def show(model_id: int) -> Response:
    body = ShowBody(model=Model(model_id))
    return app.render.ok(body=body).json()

from dataclasses import dataclass, field
from typing import List

from lf3py.api.response import Response
from lf3py.app.apiapp import ApiApp
from lf3py.app.provider import app_provider
from lf3py.routing.errors import UnresolvedArgumentsError
from lf3py.task.data import Result

app = app_provider(ApiApp)


@dataclass
class Model:
    id: int = 0


@dataclass
class IndexBody(Result):
    models: List[Model] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    model: Model = Model()


@app.entry
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@app.route('GET', '/models')
def index() -> Response:
    body = IndexBody(models=[Model(id=1234)])
    return app.render.ok(body=body).json()


@app.error(400, '400 Bad Request', UnresolvedArgumentsError)
@app.route('GET', '/models/{model_id}')
def show(model_id: int) -> Response:
    body = ShowBody(model=Model(model_id))
    return app.render.ok(body=body).json()

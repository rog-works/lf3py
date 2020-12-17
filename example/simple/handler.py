from dataclasses import dataclass, field
from typing import List

from lf2.api.errors import BadRequestError
from lf2.api.response import Response
from lf2.apps.provider import app_provider
from lf2.apps.webapp import WebApp
from lf2.task.result import Result

app = app_provider(WebApp, WebApp.default_modules())


@dataclass
class Model:
    id: int = 0


@dataclass
class IndexBody(Result):
    models: List[Model] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    model: Model = Model()


@app.webapi
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@app.route('GET', '/models')
def index() -> Response:
    body = IndexBody(models=[Model(id=1234)])
    return app.render.ok(body=body).json()


@app.error(400, '400 BadRequest', BadRequestError)
@app.route('GET', '/models/{model_id}')
def show(model_id: int) -> Response:
    body = ShowBody(model=Model(model_id))
    return app.render.ok(body=body).json()

from dataclasses import dataclass, field
from typing import List

from lf2.api.errors import BadRequestError
from lf2.api.data import Response
from lf2.apps.provider import app_provider
from lf2.apps.webapp import WebApp
from lf2.task.result import Result

app = app_provider(WebApp, WebApp.default_modules())


@app.webapi
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@dataclass
class ShowBody(Result):
    id: int = 0


@dataclass
class IndexBody(Result):
    models: List[ShowBody] = field(default_factory=list)


@app.route('GET', '/models')
def index() -> Response:
    return app.render.ok(body=IndexBody(models=[ShowBody(id=1234)]))


@app.error(400, '400 BadRequest', BadRequestError)
@app.route('GET', '/models/{model_id}')
def show(model_id: int) -> Response:
    return app.render.ok(body=ShowBody(id=model_id))

from dataclasses import dataclass, field
from typing import List

from lf2.api.types import ErrorDefinition
from lf2.api.data import Response
from lf2.api.errors import BadRequestError, ServiceUnavailableError, UnauthorizedError
from lf2.serialization.serializer import DictSerializer
from lf2.task.result import Result

from example.webapi.app import App
from example.webapi.models.user import User

app = App.get()


@app.error.custom
def errors_with(*statuses: int) -> List[ErrorDefinition]:
    defs = [
        app.error.define(401, app.i18n.trans('http.401'), ServiceUnavailableError),
        app.error.define(503, app.i18n.trans('http.503'), UnauthorizedError),
    ]
    return [(status, message, errors) for status, message, errors in defs if status in statuses]


@dataclass
class IndexBody(Result):
    success: bool = True
    users: List[User] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    success: bool = True
    user: User = field(default_factory=User)


@dataclass
class CreateParams:
    name: str = ''


CreateBody = ShowBody


@errors_with(401, 503)
@app.route('GET', '/users')
def index() -> Response:
    app.logger.info('index')

    users = User.find_all()
    return app.ok(body=IndexBody(users=users))


@app.route('GET', '/users/{user_id}')
def show(user_id: int) -> Response:
    app.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return app.ok(body=ShowBody(user=user))


@app.error.handle(400, app.i18n.trans('http.400'), BadRequestError)
@app.route('POST', '/users')
def create(params: CreateParams) -> Response:
    app.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.ok(body=CreateBody(user=user))

from dataclasses import dataclass, field
from typing import List

from example.models.user import User
from framework.api.api import ErrorDefinition
from framework.api.data import Response
from framework.api.errors import BadRequestError, ServiceUnavailableError, UnauthorizeError
from framework.app import App
from framework.serialization.serializer import DictSerializer
from framework.task.result import Result

app = App.get()


@app.api.custom_error
def errors_with(*statuses: int) -> List[ErrorDefinition]:
    defs = [
        (401, app.i18n.trans('http.401'), (ServiceUnavailableError,)),
        (503, app.i18n.trans('http.503'), (UnauthorizeError,)),
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
def index() -> Response:
    app.logger.info('index')

    users = User.find_all()
    return app.api.success(body=IndexBody(users=users))


@app.api.path_params('/users/{user_id}')
def show(user_id: int) -> Response:
    app.logger.info(f'show: {app.api.request.params}')

    user = User.find(user_id)
    return app.api.success(body=ShowBody(user=user))


@app.api.error(400, app.i18n.trans('http.400'), BadRequestError)
@app.api.params
def create(params: CreateParams) -> Response:
    app.logger.info(f'create: {app.api.request.params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.api.success(body=CreateBody(user=user))

from dataclasses import dataclass, field
from typing import List

from example.models.user import User
from framework.api.data import Response
from framework.app import App
from framework.lang.serialize import DictSerializer
from framework.task.result import Result

app = App.get()


@dataclass
class IndexBody(Result):
    success: bool = False
    users: List[User] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    success: bool = False
    user: User = field(default_factory=User)


@dataclass
class CreateParams:
    name: str = ''


CreateBody = ShowBody


def index() -> Response:
    users = User.find_all()
    return app.api.success(body=IndexBody(success=True, users=users))


@app.api.path_params('/users/{user_id}')
def show(user_id: int) -> Response:
    user = User.find(user_id)
    return app.api.success(body=ShowBody(success=True, user=user))


@app.api.error(400, app.i18n.trans('http.400'), ValueError)
@app.api.params
def create(params: CreateParams) -> Response:
    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.api.success(body=CreateBody(success=True, user=user))

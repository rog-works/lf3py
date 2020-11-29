from dataclasses import dataclass
import re

from example.models.user import User
from framework.api.data import Response
from framework.app import App
from framework.lang.serialize import DictSerializer

app = App.get()


def index() -> Response:
    users = User.find_all()
    serializer = DictSerializer()
    return app.api.success({'success': True, 'users': [serializer.serialize(user) for user in users]})


def show() -> Response:
    user_id = int(re.search(r'(\d+)$', app.api.request.path).group(1))
    user = User.find(user_id)
    serializer = DictSerializer()
    return app.api.success({'success': True, 'user': serializer.serialize(user)})


@dataclass
class CreateParams:
    name: str = ''


@app.api.error(400, app.i18n.trans('http.400'), ValueError)
@app.api.params
def create(params: CreateParams) -> Response:
    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.api.success({'success': True, 'user': serializer.serialize(user)})

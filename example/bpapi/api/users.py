from typing import List

from lf3py.api.errors import ServiceUnavailableError, UnauthorizedError
from lf3py.api.errors.types import ApiErrorDefinition
from lf3py.api.response import Response
from lf3py.routing.errors import UnresolvedArgumentsError
from lf3py.serialization.serializer import DictSerializer

from example.bpapi.app import MyApp
from example.bpapi.api.users_defs import IndexBody, ShowBody, CreateParams
from example.bpapi.models.user import User

app = MyApp.get()


@app.error.custom
def errors_with(*statuses: int) -> List[ApiErrorDefinition]:
    defs = [
        app.error.define(401, app.i18n.trans('http.401'), ServiceUnavailableError),
        app.error.define(503, app.i18n.trans('http.503'), UnauthorizedError),
    ]
    return [(status, message, errors) for status, message, errors in defs if status in statuses]


@errors_with(401, 503)
@app.route('GET', '/users')
def index() -> Response:
    app.logger.info('index')

    users = User.find_all()
    return app.render.ok(body=IndexBody(users=users)).json()


@app.route('GET', '/users/{user_id}')
def show(user_id: int) -> Response:
    app.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return app.render.ok(body=ShowBody(user=user)).json()


@app.error(400, app.i18n.trans('http.400'), UnresolvedArgumentsError)
@app.route('POST', '/users')
def create(params: CreateParams) -> Response:
    app.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.render.ok(body=ShowBody(user=user)).json()

from typing import NoReturn

from lf3py.api.errors import ApiError, BadRequestError, UnsupportedMediaTypeError
from lf3py.api.response import Response
from lf3py.middleware.api.cors import preflight_cors
from lf3py.middleware.api.error import unexpected_dispach
from lf3py.middleware.api.verifier import accept_json
from lf3py.middleware.types import ErrorMiddlewares
from lf3py.serialization.serializer import DictSerializer

from example.bpapi.app import MyApp
from example.bpapi.api.users_defs import IndexBody, ShowBody, CreateParams
from example.bpapi.models.user import User

app = MyApp.get()


def within(*statuses: int) -> ErrorMiddlewares:
    def error_400(error: BadRequestError) -> NoReturn:
        raise ApiError(app.i18n.trans('http.400'), 400) from error

    def error_415(error: UnsupportedMediaTypeError) -> NoReturn:
        raise ApiError(app.i18n.trans('http.415'), 415) from error

    handlers = {
        400: error_400,
        415: error_415,
    }
    return tuple([handler for status, handler in handlers.items() if status in statuses])


@app.behavior(preflight_cors)
@app.route('OPTION', '/')
def preflight() -> Response:
    return app.render.ok(204).json()


@app.route('GET', '/users')
def index() -> Response:
    app.logger.info('index')

    users = User.find_all()
    return app.render.ok(body=IndexBody(users=users)).json()


@app.behavior(accept_json, unexpected_dispach, error=within(400, 415))
@app.route('GET', '/users/{user_id}')
def show(user_id: int) -> Response:
    app.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return app.render.ok(body=ShowBody(user=user)).json()


@app.behavior(accept_json, unexpected_dispach, error=within(400, 415))
@app.route('POST', '/users')
def create(params: CreateParams) -> Response:
    app.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.render.ok(body=ShowBody(user=user)).json()

from lf3py.api.response import Response
from lf3py.middleware.api.cors import preflight_cors
from lf3py.middleware.api.error import unexpected_dispach
from lf3py.middleware.api.verifier import accept_json
from lf3py.serialization.serializer import DictSerializer

from example.bpapi.app import MyApp
from example.bpapi.api.users_defs import IndexBody, ShowBody, CreateParams
from example.bpapi.middleware.error import within
from example.bpapi.models.user import User
from example.bpapi.session import Session

session = Session()
bp = MyApp.blueprint()


@bp.behavior(preflight_cors)
@bp.api.option('/')
def preflight() -> Response:
    return session.render.ok(204).json()


@bp.api.get('/users')
def index() -> Response:
    session.logger.info('index')

    users = User.find_all()
    return session.render.ok(body=IndexBody(users=users)).json()


@bp.behavior(accept_json)
@bp.on_error(unexpected_dispach, *within(400, 415))
@bp.api.get('/users/{user_id}')
def show(user_id: int) -> Response:
    session.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return session.render.ok(body=ShowBody(user=user)).json()


@bp.behavior(accept_json)
@bp.on_error(unexpected_dispach, *within(400, 415))
@bp.api.post('/users')
def create(params: CreateParams) -> Response:
    session.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return session.render.ok(body=ShowBody(user=user)).json()

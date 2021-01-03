from lf3py.api.response import Response
from lf3py.middleware.api import accepts, changes, preflights, statuses
from lf3py.serialization.serializer import DictSerializer

from example.bpapi.app import MyApp
from example.bpapi.api.users_defs import IndexBody, ShowBody, CreateParams
from example.bpapi.models.user import User
from example.bpapi.session import MySession

session = MySession()
bp = MyApp.blueprint()


@bp.behavior(preflights.cors)
@bp.api.option('/')
def preflight() -> Response:
    return session.render.ok(204).json()


@bp.api.get('/users')
def index() -> Response:
    session.logger.info('index')

    users = User.find_all()
    return session.render.ok(body=IndexBody(users=users)).json()


@bp.on_error(changes.fail_dispach_to_400)
@bp.api.produce(accepts.json)
@bp.api.output(*statuses.on(400, 415))
@bp.api.get('/users/{user_id}')
def show(user_id: int) -> Response:
    session.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return session.render.ok(body=ShowBody(user=user)).json()


@bp.on_error(changes.fail_dispach_to_400)
@bp.api.produce(accepts.json)
@bp.api.output(*statuses.on(400, 415))
@bp.api.post('/users')
def create(params: CreateParams) -> Response:
    session.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return session.render.ok(body=ShowBody(user=user)).json()

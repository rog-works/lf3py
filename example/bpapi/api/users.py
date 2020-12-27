from lf3py.api.response import Response
from lf3py.middleware.api.cors import preflight_cors
from lf3py.middleware.api.error import unexpected_dispach
from lf3py.middleware.api.verifier import accept_json
from lf3py.serialization.serializer import DictSerializer

from example.bpapi.app import MyApp
from example.bpapi.api.users_defs import IndexBody, ShowBody, CreateParams
from example.bpapi.middleware.error import within
from example.bpapi.models.user import User

app = MyApp.instance()


@app.behavior(preflight_cors)
@app.api.option('/')
def preflight() -> Response:
    return app.render.ok(204).json()


@app.api.get('/users')
def index() -> Response:
    app.logger.info('index')

    users = User.find_all()
    return app.render.ok(body=IndexBody(users=users)).json()


@app.behavior(accept_json, error=(unexpected_dispach, *within(400, 415)))
@app.api.get('/users/{user_id}')
def show(user_id: int) -> Response:
    app.logger.info(f'show: user_id = {user_id}')

    user = User.find(user_id)
    return app.render.ok(body=ShowBody(user=user)).json()


@app.behavior(accept_json, error=(unexpected_dispach, *within(400, 415)))
@app.api.post('/users')
def create(params: CreateParams) -> Response:
    app.logger.info(f'create: params = {params}')

    serializer = DictSerializer()
    user = User.create(**serializer.serialize(params))
    return app.render.ok(body=ShowBody(user=user)).json()

from lf3py.api.response import Response
from lf3py.app.apiapp import ApiApp
from lf3py.middleware.api import changes, statuses

from example.inlineapi.model_defs import IndexBody, Model, ShowBody


def handler(event: dict, context: object) -> dict:
    app = ApiApp.entry(event)

    def run() -> dict:
        try:
            return app.run().serialize()
        except Exception as e:
            return app.render.fail(e).json().serialize()

    @app.api.get('/models')
    def index() -> Response:
        body = IndexBody(models=[Model(id=1234)])
        return app.render.ok(body=body).json()

    @app.on_error(changes.dispatch_error_to_400)
    @app.schema.error(statuses.bad_request)
    @app.api.get('/models/{model_id}')
    def show(model_id: int) -> Response:
        body = ShowBody(model=Model(model_id))
        return app.render.ok(body=body).json()

    return run()

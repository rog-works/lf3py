from abc import ABCMeta

from lf3py.api.request import Request
from lf3py.task.data import Result
from lf3py.task.types import RunnerDecorator


class IApiRouter(metaclass=ABCMeta):
    def get(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.get('/models')
            >>> def index() -> Response:
            >>>     body = IndexBody(Model.all())
            >>>     return app.render.ok(body=body).json()

            >>> @app.api.get('/models/{id}')
            >>> def show(id: int) -> Response:
            >>>     body = ShowBody(Model.find(id))
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    def post(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.post('/models')
            >>> def create(params: CreateParams) -> Response:
            >>>     model = Model.create(params)
            >>>     body = ShowBody(model)
            >>>     return app.render.ok(status=201, body=body).json()
        """
        raise NotImplementedError()

    def put(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.put('/models/{model_id}')
            >>> def create(model_id: int, params: UpdateParams) -> Response:
            >>>     model = Model.find(model_id)
            >>>     model.update_attributes(params)
            >>>     model.save()
            >>>     body = ShowBody(model)
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    def delete(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.delete('DELETE', '/models/{model_id}')
            >>> def delete(model_id: int) -> Response:
            >>>     model = Models.find(model_id)
            >>>     model.delete()
            >>>     body = DeleteBody(model_id)
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    def patch(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.patch('/models/{model_id}')
            >>> def patch(model_id: int, params: PatchParams) -> Response:
            >>>     model = Model.find(model_id)
            >>>     model.update_attributes(params)
            >>>     model.save()
            >>>     body = ShowBody(model)
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    def option(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.behavior(preflight_cors)
            >>> @app.api.option('/')
            >>> def option() -> Response:
            >>>     return app.render.ok(status=204).json()
        """
        raise NotImplementedError()

    def dispatch(self, request: Request) -> Result:
        raise NotImplementedError()

from abc import ABCMeta

from lf3py.api.request import Request
from lf3py.task.result import Result
from lf3py.task.types import RunnerDecorator


class IApiRouter(metaclass=ABCMeta):
    def __call__(self, method: str, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.route('GET', '/models')
            >>> def index() -> Response:
            >>>     return app.render.ok(body=IndexBody(Model.find_all()))

            >>> @app.route('GET', '/models/{id}')
            >>> def show(id: int) -> Response:
            >>>     return app.render.ok(body=ShowBody(Model.find(id)))

            >>> @app.route('POST', '/models')
            >>> def create(params: CreateParams) -> Response:
            >>>     return app.render.ok(body=ShowBody(Model.create(params)))

            >>> @app.route('DELETE', '/models/{id}')
            >>> def delete(id: int) -> Response:
            >>>     Models.find(id).delete()
            >>>     return app.render.ok()
        """
        raise NotImplementedError()

    def dispatch(self, request: Request) -> Result:
        raise NotImplementedError()

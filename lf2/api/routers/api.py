from abc import ABCMeta

from lf2.api.request import Request
from lf2.task.result import Result
from lf2.task.router import Router
from lf2.task.types import RunnerDecorator


class ApiRouter(Router, metaclass=ABCMeta):
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

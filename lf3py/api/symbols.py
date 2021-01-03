from abc import ABCMeta, abstractmethod

from lf3py.api.response import Response
from lf3py.middleware.types import AttachMiddleware, CatchMiddleware
from lf3py.routing.symbols import IRouter
from lf3py.task.data import Result
from lf3py.task.types import RunnerDecorator
from lf3py.view.symbols import IRender


class IApiRender(IRender):
    @abstractmethod
    def ok(self, status: int = 200, body: Result = Result()) -> Response:
        raise NotImplementedError()

    @abstractmethod
    def fail(self, error: Exception) -> Response:
        raise NotImplementedError()


class IApiRouter(IRouter):
    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def option(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.behavior(preflight_cors)
            >>> @app.api.option('/')
            >>> def option() -> Response:
            >>>     return app.render.ok(status=204).json()
        """
        raise NotImplementedError()

    @abstractmethod
    def head(self, path_spec: str) -> RunnerDecorator:
        """
        Examples:
            >>> @app.api.head('/')
            >>> def head() -> Response:
            >>>     return app.render.ok().json()
        """
        raise NotImplementedError()


class IApiSchema(metaclass=ABCMeta):
    @abstractmethod
    def consume(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        """
        Examples:
            >>> @app.schema.consume(content_types.json)
            >>> @app.api.get('/models')
            >>> def index() -> Response:
            >>>     body = IndexBody(Model.all())
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    @abstractmethod
    def produce(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        """
        Examples:
            >>> @app.schema.produce(accepts.json)
            >>> @app.api.get('/models')
            >>> def index() -> Response:
            >>>     body = IndexBody(Model.all())
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    @abstractmethod
    def secutity(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        """
        Examples:
            >>> @app.schema.security(securities.jwt)
            >>> @app.api.get('/models')
            >>> def index() -> Response:
            >>>     body = IndexBody(Model.all())
            >>>     return app.render.ok(body=body).json()
        """
        raise NotImplementedError()

    @abstractmethod
    def header(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        """
        Examples:
            >>> @app.schema.header(preflights.cors)
            >>> @app.api.option('/')
            >>> def preflight() -> Response:
            >>>     return app.render.ok(status=204).json()
        """
        raise NotImplementedError()

    @abstractmethod
    def error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        """
        Examples:
            >>> @app.on_error(changes.dispatch_error_to_400)
            >>> @app.schema.error(statuses.bad_request)
            >>> @app.api.post('/models')
            >>> def create(params: ModelParams) -> Response:
            >>>     model = Model.create(params)
            >>>     body = ShowBody(model)
            >>>     return app.render.ok(status=201, body=body).json()
        """
        raise NotImplementedError()

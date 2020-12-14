from lf2.api.presenter import ApiErrorPresenter, ApiOkPresenter
from lf2.api.data import Request
from lf2.api.route import ApiRoute
from lf2.apps.app import App
from lf2.apps.definitions import webapi_modules
from lf2.aws.types import LambdaHandler
from lf2.aws.aws_lambda.decode import decode_request
from lf2.task.result import Result
from lf2.task.runner import Runner


class WebApp(App):
    @classmethod
    def default_modules(cls) -> dict:
        return webapi_modules()

    @property
    def route(self) -> ApiRoute:
        return self._di.resolve(ApiRoute)

    @property
    def ok(self) -> ApiOkPresenter:
        return self._di.resolve(ApiOkPresenter)

    @property
    def error(self) -> ApiErrorPresenter:
        return self._di.resolve(ApiErrorPresenter)

    def run(self) -> Result:
        return self.perform(Runner)

    def webapi(self, handler: LambdaHandler) -> LambdaHandler:
        def wrapper(event: dict, context: object) -> dict:
            self._di.register(Request, lambda: decode_request(event))
            return handler(event, context)

        return wrapper

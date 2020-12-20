from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.sns.record import SNSRecord
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.routing.routers import Router
from lf3py.task.data import Result


class SNSApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return sns_modules()

    @property
    def route(self) -> Router:
        return self._di.resolve(Router)

    def run(self) -> Result:
        for record in self._di.resolve(LambdaEvent):
            command = SNSRecord.deserialize(record)
            self.route.dispatch(command)

        return Result()  # XXX unnecessary result

    @hook
    def entry(self, event: dict, context: object):
        self._di.register(LambdaEvent, lambda: event)

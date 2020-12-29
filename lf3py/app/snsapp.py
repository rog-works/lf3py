from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.sns.record import SNSRecords
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.routing.symbols import IRouter
from lf3py.task.data import Result, Ok


class SNSApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return sns_modules()

    @property
    def route(self) -> IRouter:
        return self._locator.resolve(IRouter)

    def run(self) -> Result:
        with self.start():
            for record in self._locator.resolve(SNSRecords):
                self.route.dispatch(record)

        return Ok

    @hook
    def entry(self, event: dict, context: object):
        self._locator.register(LambdaEvent, lambda: event)

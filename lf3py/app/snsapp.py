from lf3py.session.locator import Locatorify
from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.aws.hooks.method import hook
from lf3py.aws.sns.record import SNSRecords
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.routing.routers.types import IRouter
from lf3py.session.session import Session
from lf3py.task.data import Result, Ok


class SNSApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return sns_modules()

    @property
    def route(self) -> IRouter:
        return self._di.resolve(IRouter)

    def run(self) -> Result:
        with self._di.resolve(Session):
            for record in self._di.resolve(SNSRecords):
                self.route.dispatch(record)

        return Ok

    @hook
    def entry(self, event: dict, context: object):
        self._di.register(Session, lambda: Session(Locatorify(self._di.resolve)))
        self._di.register(LambdaEvent, lambda: event)

from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.aws.sns.record import SNSRecords
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
        with self.start() as session:
            for record in session(SNSRecords):
                with self.middleware.attach(session, self.route, record):
                    self.route.dispatch(record)

        return Ok

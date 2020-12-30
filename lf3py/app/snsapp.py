from lf3py.app.app import App
from lf3py.app.definitions import sns_modules
from lf3py.aws.sns.record import SNSRecords
from lf3py.config import ModuleDefinitions
from lf3py.routing.symbols import IDispatcher, IRouter
from lf3py.task.data import Result, Ok


class SNSApp(App):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return sns_modules()

    @property
    def route(self) -> IRouter:
        return self._locator.resolve(IRouter)

    @property
    def dispatcher(self) -> IDispatcher:
        return self._locator.resolve(IDispatcher)

    def run(self) -> Result:
        for record in self._locator.resolve(SNSRecords):
            self.dispatcher.dispatch(record, self.route)

        return Ok

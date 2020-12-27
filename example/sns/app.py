import example.sns.preprocess  # noqa F401

from lf3py.app.snsapp import SNSApp
from lf3py.aws.symbols import IFireHose
from lf3py.config.types import ModuleDefinitions

from example.sns.modules import modules


class MyApp(SNSApp):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        return modules()

    @property
    def firehose(self) -> IFireHose:
        return self._di.resolve(IFireHose)

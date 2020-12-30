import example.sns.preprocess  # noqa F401

from lf3py.app.snsapp import SNSApp
from lf3py.aws.symbols import IFireHose
from lf3py.config.types import ModuleDefinitions

from example.sns.modules import add_modules


class MyApp(SNSApp):
    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        base = super(MyApp, cls).module_definitions()
        return {**base, **add_modules()}

    @property
    def firehose(self) -> IFireHose:
        return self._locator.resolve(IFireHose)

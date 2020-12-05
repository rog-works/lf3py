from logging import Logger

from framework.api.api import Api
from framework.api.data import Request, Response
from framework.app import App
from framework.aws.aws_lambda.decode import decode_request
from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.lang.di import DI
from framework.lang.module import load_module
from framework.task.runner import Runner

from example.config.routes import Routes


def aws_app(event: dict, _: object) -> App:
    di = DI()
    di.register(Request, lambda: decode_request(event))
    di.register(Response, lambda: Response(headers={'Content-Type': 'application/json'}))
    di.register(Config, lambda: load_module('example.config.config', 'config'))
    di.register(Routes, lambda: load_module('example.config.routes', 'routes'))
    di.register(Logger, load_module('example.provider.logger', 'make_logger'))
    di.register(I18n, load_module('example.provider.i18n', 'make_i18n'))
    di.register(Runner, load_module('example.provider.runner', 'resolve'))
    di.register(Api, Api)
    return App.create(di)

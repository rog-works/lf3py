from logging import Logger

from framework.api.api import Api, ErrorHandler
from framework.api.data import Request, Response
from framework.aws.aws_lambda.decode import decode_request
from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.lang.cache import Cache
from framework.lang.di import DI
from framework.lang.module import load_module
from framework.task.runner import Runner

from example.app import App
from example.config.routes import Routes


def aws_app(event: dict, _: object) -> App:
    di = DI()
    di.register(Api, Api)
    di.register(Cache, load_module('example.provider.cache', 'make_cache'))
    di.register(Config, load_module('example.config.config', 'config'))
    di.register(ErrorHandler, load_module('example.provider.error_handler', 'make_error_handler'))
    di.register(I18n, load_module('example.provider.i18n', 'make_i18n'))
    di.register(Logger, load_module('example.provider.logger', 'make_logger'))
    di.register(Request, lambda: decode_request(event))
    di.register(Response, load_module('example.provider.response', 'make_response'))
    di.register(Routes, load_module('example.config.routes', 'routes'))
    di.register(Runner, load_module('example.provider.runner', 'resolve'))
    return App.create(di)

from logging import Logger

from framework.app import App
from framework.aws.aws_lambda.decode import decode_request
from framework.data.config import Config
from framework.http.data import Request, Response
from framework.i18n.locale import Locale
from framework.lang.di import DI
from framework.lang.module import load_module
from framework.task.runner import Runner


def aws_app(event: dict, _: object) -> App:
    di = DI()
    di.register(Request, lambda: decode_request(event))
    di.register(Response, lambda: Response(headers={'Content-Type': 'application/json'}))
    di.register(Config, lambda: load_module('example.config', 'config'))
    di.register(Logger, load_module('example.logger', 'make_logger'))
    di.register(Locale, load_module('example.i18n', 'make_locale'))
    di.register(Runner, lambda: load_module('example.router', 'resolve'))
    return App(__name__, di)

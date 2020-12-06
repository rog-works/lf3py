from framework.api.api import ErrorHandler
from framework.data.config import Config
from framework.lang.module import load_module


def make_error_handler(config: Config) -> ErrorHandler:
    module_name = config['error_handler']['module']
    definition = config['error_handler']['modules'][module_name]
    return load_module(definition['path'], definition['module'])

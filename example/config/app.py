import os

from framework.app import App


def app_defifintion() -> dict:
    return {
        'app': 'example.app.App',
        'modules': {
            'Api': 'framework.api.api.Api',
            'framework.lang.cache.Cache': 'framework.lang.cache.Cache',
            'framework.data.Config': 'example.config.config',
            'framework.api.api.ErrorHandler': os.environ.get('MODULES_ERROR_HANDLER', 'example.api.error_handler.dev_handler'),
            'framework.i18n.i18n.I18n': 'example.provider.i18n.make_i18n',
            'logging.Logger': 'example.provider.make_logger',
            'framework.api.data.Request': 'example.provider.request.make_request',
            'example.config.routes.Routes': 'example.config.routes.routes',
            'framework.task.runner.Runner': 'example.provider.runner.resolve',
            'Storage': 'framework.lang.cache.Storage',
        },
    }


def app_provider(definition: dict) -> App:
    load_module()

import os


def modules() -> dict:
    return {
        'api': 'framework.api.api.Api',
        'cache': 'framework.lang.cache.Cache',
        'framework.api.types.ErrorHandler': os.environ.get('MODULES_ERROR_HANDLER', 'example.provider.error_handler.make_dev_handler'),
        'framework.api.data.Response': 'example.provider.response.make_response',
        'framework.data.config.Config': 'example.config.config.config',
        'framework.i18n.i18n.I18n': 'example.provider.i18n.make_i18n',
        'framework.task.router.Router': 'example.provider.router.make_router',
        'framework.task.router.Routes': 'example.config.routes.routes',
        'framework.task.runner.Runner': 'example.provider.runner.resolve',
        'logging.Logger': 'example.provider.logger.dev_logger',
        'storage': 'framework.lang.cache.Storage',
    }

import os


def modules() -> dict:
    return {
        'api': 'lf2.api.api.Api',
        'cache': 'lf2.lang.cache.Cache',
        'lf2.api.types.ErrorHandler': os.environ.get('MODULES_ERROR_HANDLER', 'example.webapi.provider.error_handler.make_dev_handler'),
        'lf2.api.data.Response': 'example.webapi.provider.response.make_response',
        'lf2.data.config.Config': 'example.webapi.config.config.config',
        'lf2.i18n.i18n.I18n': 'example.webapi.provider.i18n.make_i18n',
        'lf2.task.router.Router': 'example.webapi.provider.router.make_router',
        'lf2.task.router.Routes': 'example.webapi.config.routes.routes',
        'lf2.task.runner.Runner': 'example.webapi.provider.runner.resolve',
        'logging.Logger': 'example.webapi.provider.logger.dev_logger',
        'storage': 'lf2.lang.cache.Storage',
    }

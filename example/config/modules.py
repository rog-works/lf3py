import os


def modules() -> dict:
    return {
        'example.config.routes.Routes': 'example.config.routes.routes',
        'framework.api.api.Api': 'framework.api.api.Api',
        'framework.api.api.ErrorHandler': os.environ.get('MODULES_ERROR_HANDLER', 'example.provider.error_handler.make_dev_handler'),
        'framework.api.data.Response': 'example.provider.response.make_response',
        'framework.data.config.Config': 'example.config.config.config',
        'framework.i18n.i18n.I18n': 'example.provider.i18n.make_i18n',
        'framework.lang.cache.Cache': 'framework.lang.cache.Cache',
        'framework.lang.cache.Storage': 'framework.lang.cache.Storage',
        'framework.task.runner.Runner': 'example.provider.runner.resolve',
        'logging.Logger': 'example.provider.logger.dev_logger',
    }

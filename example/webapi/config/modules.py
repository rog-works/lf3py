import os


def modules() -> dict:
    return {
        'lf2.api.request.Request': 'lf2.api.provider.request',
        'lf2.api.response.Response': 'example.webapi.provider.response.make_response',
        'lf2.api.errors.handler.ApiErrorHandler': 'lf2.api.errors.handler.ApiErrorHandler',
        'lf2.api.render.ApiRender': os.environ.get('MODULES_RENDER', 'lf2.api.render.ApiRender'),
        'lf2.api.routers.api.IApiRouter': 'lf2.api.routers.bp.BpRouter',
        'lf2.data.config.Config': 'example.webapi.config.config.config',
        'lf2.lang.cache.Cache': 'lf2.lang.cache.Cache',
        'lf2.i18n.i18n.I18n': 'example.webapi.provider.i18n.make_i18n',
        'lf2.task.types.Routes': 'example.webapi.config.routes.routes',
        'logging.Logger': 'example.webapi.provider.logger.dev_logger',
    }

import os


def modules() -> dict:
    return {
        'example.bpapi.data.context.MyContext': 'example.bpapi.provider.context.make_context',
        'lf2.api.render.ApiRender': os.environ.get('MODULES_RENDER', 'lf2.api.render.ApiRender'),
        'lf2.api.request.Request': 'lf2.api.provider.request',
        'lf2.api.response.Response': 'example.bpapi.provider.response.make_response',
        'lf2.api.errors.handler.ApiErrorHandler': 'lf2.api.errors.handler.ApiErrorHandler',
        'lf2.api.routers.api.IApiRouter': 'lf2.api.routers.bp.BpRouter',
        'lf2.data.config.Config': 'example.bpapi.config.config.config',
        'lf2.lang.cache.Cache': 'lf2.lang.cache.Cache',
        'lf2.i18n.i18n.I18n': 'example.bpapi.provider.i18n.make_i18n',
        'lf2.task.types.Routes': 'example.bpapi.config.routes.routes',
        'logging.Logger': 'example.bpapi.provider.logger.dev_logger',
    }

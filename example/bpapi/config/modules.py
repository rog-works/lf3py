import os


def modules() -> dict:
    return {
        'example.bpapi.data.context.MyContext': 'example.bpapi.provider.context.make_context',
        'lf3py.api.render.ApiRender': os.environ.get('MODULES_RENDER', 'lf3py.api.render.ApiRender'),
        'lf3py.api.response.Response': 'example.bpapi.provider.response.make_response',
        'lf3py.api.errors.handler.ApiErrorHandler': 'lf3py.api.errors.handler.ApiErrorHandler',
        'lf3py.api.router.IApiRouter': 'lf3py.routing.routers.bp.BpRouter',
        'lf3py.config.Config': 'example.bpapi.config.config.config',
        'lf3py.config.Routes': 'example.bpapi.config.routes.routes',
        'lf3py.i18n.i18n.I18n': 'example.bpapi.provider.i18n.make_i18n',
        'lf3py.lang.cache.Cache': 'lf3py.lang.cache.Cache',
        'lf3py.task.data.Command': 'lf3py.api.provider.request',
        'logging.Logger': 'example.bpapi.provider.logger.dev_logger',
    }

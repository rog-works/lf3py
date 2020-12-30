import os


def modules() -> dict:
    return {
        'example.bpapi.data.context.MyContext': 'example.bpapi.provider.context.make_context',
        'lf3py.api.request.Request': 'lf3py.api.provider.request',
        'lf3py.api.response.Response': 'example.bpapi.provider.response.make_response',
        'lf3py.api.symbols.IApiRender': os.environ.get('MODULES_RENDER', 'lf3py.api.render.ApiRender'),
        'lf3py.api.symbols.IApiRouter': 'lf3py.api.router.BpApiRouter',
        'lf3py.cache.Cache': 'lf3py.cache.Cache',
        'lf3py.config.Config': 'example.bpapi.config.config.config',
        'lf3py.config.Routes': 'example.bpapi.config.routes.routes',
        'lf3py.i18n.I18n': 'example.bpapi.provider.i18n.make_i18n',
        'lf3py.middleware.Middleware': 'lf3py.middleware.Middleware',
        'lf3py.routing.dispatcher.Dispatcher': 'lf3py.routing.dispatcher.BpDispatcher',
        'logging.Logger': 'example.bpapi.provider.logger.dev_logger',
    }

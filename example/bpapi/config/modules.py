import os


def add_modules() -> dict:
    return {
        'example.bpapi.data.context.MyContext': 'example.bpapi.provider.context.make_context',
        'lf3py.api.response.Response': 'example.bpapi.provider.response.make_response',
        'lf3py.api.symbols.IApiRender': os.environ.get('MODULES_RENDER', 'lf3py.api.render.ApiRender'),
        'lf3py.cache.Cache': 'lf3py.cache.Cache',
        'lf3py.config.Config': 'example.bpapi.config.config.config',
        'lf3py.config.Routes': 'example.bpapi.config.routes.routes',
        'lf3py.i18n.I18n': 'example.bpapi.provider.i18n.make_i18n',
        'logging.Logger': 'example.bpapi.provider.logger.dev_logger',
    }

def flowapi_modules() -> dict:
    return {
        'lf3py.api.errors.handler.ApiErrorHandler': 'lf3py.api.errors.handler.ApiErrorHandler',
        'lf3py.api.render.ApiRender': 'lf3py.api.render.ApiRender',
        'lf3py.api.request.Request': 'lf3py.api.provider.request',
        'lf3py.api.response.Response': 'lf3py.api.response.Response',
        'lf3py.api.routers.api.IApiRouter': 'lf3py.api.routers.flow.FlowRouter',
    }

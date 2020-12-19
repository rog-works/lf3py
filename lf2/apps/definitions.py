def webapp_modules() -> dict:
    return {
        'lf2.api.errors.handler.ApiErrorHandler': 'lf2.api.errors.handler.ApiErrorHandler',
        'lf2.api.render.ApiRender': 'lf2.api.render.ApiRender',
        'lf2.api.request.Request': 'lf2.api.provider.request',
        'lf2.api.response.Response': 'lf2.api.response.Response',
        'lf2.api.routers.api.ApiRouter': 'lf2.api.routers.flow.FlowRouter',
    }

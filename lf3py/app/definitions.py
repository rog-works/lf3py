def flowapi_modules() -> dict:
    return {
        'lf3py.api.errors.handler.ApiErrorHandler': 'lf3py.api.errors.handler.ApiErrorHandler',
        'lf3py.api.render.ApiRender': 'lf3py.api.render.ApiRender',
        'lf3py.api.request.Request': 'lf3py.api.provider.request',
        'lf3py.api.response.Response': 'lf3py.api.response.Response',
        'lf3py.api.router.IApiRouter': 'lf3py.api.provider.flow_router',
    }


def sns_modules() -> dict:
    return {
        'lf3py.routing.routers.Router': 'lf3py.routing.routers.flow.FlowRouter',
        'lf3py.aws.sns.record.SNSRecords': 'lf3py.aws.sns.provider.records',
    }

def flowapi_modules() -> dict:
    return {
        'lf3py.api.errors.handler.ApiErrorHandler': 'lf3py.api.errors.handler.ApiErrorHandler',
        'lf3py.api.render.ApiRender': 'lf3py.api.render.ApiRender',
        'lf3py.api.response.Response': 'lf3py.api.response.Response',
        'lf3py.api.router.IApiRouter': 'lf3py.routing.routers.flow.FlowRouter',
        'lf3py.lang.dsn.DSNType': 'lf3py.api.provider.api_dsn_type',
        'lf3py.task.data.Command': 'lf3py.api.provider.request',
    }


def sns_modules() -> dict:
    return {
        'lf3py.routing.routers.Router': 'lf3py.routing.routers.flow.FlowRouter',
        'lf3py.aws.sns.record.SNSRecords': 'lf3py.aws.sns.provider.records',
    }

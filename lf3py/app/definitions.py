def bpapi_modules() -> dict:
    return {
        'lf3py.api.request.Request': 'lf3py.api.provider.request',
        'lf3py.api.response.Response': 'lf3py.api.response.Response',
        'lf3py.api.Api': 'lf3py.api.Api',
        'lf3py.api.symbols.IApiRender': 'lf3py.api.render.ApiRender',
        'lf3py.api.symbols.IApiRouter': 'lf3py.api.router.BpApiRouter',
        'lf3py.config.Routes': 'lf3py.config.Routes',
        'lf3py.middleware.Middleware': 'lf3py.middleware.Middleware',
        'lf3py.task.TaskQueue': 'lf3py.app.provider.single_task_queue',
    }


def inlineapi_modules() -> dict:
    return {
        'lf3py.api.request.Request': 'lf3py.api.provider.request',
        'lf3py.api.response.Response': 'lf3py.api.response.Response',
        'lf3py.api.Api': 'lf3py.api.Api',
        'lf3py.api.symbols.IApiRender': 'lf3py.api.render.ApiRender',
        'lf3py.api.symbols.IApiRouter': 'lf3py.api.router.InlineApiRouter',
        'lf3py.middleware.Middleware': 'lf3py.middleware.Middleware',
        'lf3py.task.TaskQueue': 'lf3py.app.provider.single_task_queue',
    }


def sns_modules() -> dict:
    return {
        'lf3py.aws.sns.record.SNSRecords': 'lf3py.aws.sns.decode.decode_records',
        'lf3py.middleware.Middleware': 'lf3py.middleware.Middleware',
        'lf3py.routing.symbols.IRouter': 'lf3py.routing.router.InlineRouter',
        'lf3py.task.TaskQueue': 'lf3py.app.provider.sns_task_queue',
    }

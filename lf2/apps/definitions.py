def webapi_modules() -> dict:
    return {
        'error': 'lf2.api.error.ApiErrorHandler',
        'lf2.task.runner.Runner': 'lf2.api.provider.runner',
        'render': 'lf2.api.render.ApiRender',
        'request': 'lf2.api.request.Request',
        'response': 'lf2.api.response.Response',
        'route': 'lf2.api.route.ApiRoute',
        'router': 'lf2.task.router.Router',
    }

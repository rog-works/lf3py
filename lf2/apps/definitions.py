def webapi_modules() -> dict:
    return {
        'error': 'lf2.api.error.ApiErrorHandler',
        'lf2.task.runner.Runner': 'lf2.api.provider.runner',
        'render': 'lf2.api.render.ApiRender',
        'response': 'lf2.api.data.Response',
        'route': 'lf2.api.route.ApiRoute',
        'router': 'lf2.task.router.Router',
    }

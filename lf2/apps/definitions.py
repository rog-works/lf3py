def webapi_modules() -> dict:
    return {
        'error': 'lf2.api.presenter.ApiErrorPresenter',
        'lf2.task.runner.Runner': 'lf2.api.provider.runner',
        'ok': 'lf2.api.presenter.ApiOkPresenter',
        'response': 'lf2.api.data.Response',
        'route': 'lf2.api.route.ApiRoute',
        'router': 'lf2.task.router.Router',
    }

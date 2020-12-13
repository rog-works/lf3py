import os


def modules() -> dict:
    return {
        'cache': 'lf2.lang.cache.Cache',
        'lf2.api.data.Response': 'example.webapi.provider.response.make_response',
        'lf2.api.presenter.ApiErrorPresenter': os.environ.get('MODULES_ERROR', 'lf2.api.presenter.ApiErrorPresenter'),
        'lf2.data.config.Config': 'example.webapi.config.config.config',
        'lf2.i18n.i18n.I18n': 'example.webapi.provider.i18n.make_i18n',
        'lf2.task.router.Router': 'example.webapi.provider.router.make_router',
        'lf2.task.router.Routes': 'example.webapi.config.routes.routes',
        'lf2.task.runner.Runner': 'example.webapi.provider.runner.resolve',
        'logging.Logger': 'example.webapi.provider.logger.dev_logger',
        'ok': 'lf2.api.presenter.ApiOkPresenter',
        'route': 'lf2.api.route.ApiRoute',
        'storage': 'lf2.lang.cache.Storage',
    }

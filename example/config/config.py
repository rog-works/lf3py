import os


def config() -> dict:
    {
        'env': os.environ.get('ENV', 'local'),
        'app': {
            'module': 'example.app.App',
            'symbol_path': 'modules.symbols',
            'inject_path': 'modules.injects',
            'dependeds': {
                'api': 'api',
                'cache': 'cache',
                'config': 'config',
                'error_handler': os.environ.get('ERROR_HANDLER_MODULE', 'error_handler.dev'),
                'i18n': 'i18n',
                'logger': 'logger',
                'request': 'request',
                'response': 'response',
                'routes': 'routes',
                'runner': 'runner',
                'storage': 'storage',
            },
        },
        'modules': {
            'symbols': {
                'api': 'framework.api.api.Api',
                'cache': 'framework.lang.cache.Cache',
                'config': 'framework.data.Config',
                'error_handler': 'framework.api.api.ErrorHandler',
                'i18n': 'framework.i18n.i18n.I18n',
                'logger': 'logging.Logger',
                'request': 'framework.api.data.Request',
                'response': 'framework.api.data.Response',
                'routes': 'example.config.routes.Routes',
                'runner': 'framework.task.runner.Runner',
                'storage': 'framework.lang.cache.Storage',
            },
            'injects': {
                'api': 'framework.api.api.Api',
                'cache': 'framework.lang.cache.Cache',
                'config': 'example.config.config',
                'error_handler': {
                    'dev': 'example.api.error_handler.dev_handler',
                    'prd': 'example.api.error_handler.prd_handler',
                },
                'i18n': {
                    'module': 'example.provider.i18n.make_i18n',
                    'extra': {
                        'default_locale': 'ja',
                        'config_path': 'example.config.trans.{}',
                    },
                },
                'logger': {
                    'module': 'example.provider.make_logger',
                    'extra': {
                        'level': 'DEBUG',
                        'path': 'example/logs/app.log',
                        'format': '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
                    },
                },
                'request': 'example.provider.request.make_request',
                'response': {
                    'module': 'example.provider.response.make_response',
                    'extra': {
                        'headers': {'Content-Type': 'application/json'},
                    },
                },
                'routes': 'example.config.routes.routes',
                'runner': 'example.provider.runner.resolve',
                'storage': 'framework.lang.cache.Storage',
            },
        },
    }
    return {
        'env': os.environ.get('ENV', 'local'),
        'logger': {
            'module': os.environ.get('LOGGER_MODULE', 'dev_handler'),
            'modules': {
                'dev_handler': {
                    'level': 'DEBUG',
                    'path': 'example/logs/app.log',
                    'format': '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
                },
                'prd_handler': {
                    'dsn': 'https://example.com/xxx@hoge',
                },
            },
        },
        'response': {
            'headers': {'Content-Type': 'application/json'},
        },
        'i18n': {
            'locale': {
                'default': 'ja',
            },
            'trans': {
                'path': 'example.config.trans.{}',
                'module': 'config',
            },
        },
        'error_handler': {
            'module': os.environ.get('ERROR_HANDLER_MODULE', 'dev_handler'),
            'modules': {
                'dev_handler': {
                    'path': 'example.api.error_handler',
                    'module': 'dev_handler',
                },
                'prd_handler': {
                    'path': 'example.api.error_handler',
                    'module': 'prd_handler',
                },
            },
        },
        'cache': {
            'module': os.environ.get('CACHE_MODULE', 'dev_cache'),
            'modules': {
                'dev_cache': {},
                'prd_cache': {
                    'host': 'xxx.xxx.xxx.xxx',
                    'port': 1234,
                    'user': 'hoge',
                    'password': 'fuga',
                },
            },
        },
    }

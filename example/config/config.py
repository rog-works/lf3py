import os


def config() -> dict:
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

import os


def config() -> dict:
    return {
        'env': os.environ.get('ENV', 'local'),
        'logger': {
            'dev_handler': {
                'level': 'DEBUG',
                'path': 'example/logs/app.log',
                'format': '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
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
            'dev_handler': {
                'path': 'example.api.error_handler',
                'module': 'dev_handler',
            },
            'prd_handler': {
                'path': 'example.api.error_handler',
                'module': 'prd_handler',
            },
        },
        'cache': {
            'dev_cache': {},
            'prd_cache': {
                'host': 'xxx.xxx.xxx.xxx',
                'port': 1234,
                'user': 'hoge',
                'password': 'fuga',
            },
        },
    }

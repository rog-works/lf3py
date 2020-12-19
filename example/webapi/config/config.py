import os


def config() -> dict:
    return {
        'env': os.environ.get('ENV', 'local'),
        'logger': {
            'dev_handler': {
                'level': 'DEBUG',
                'path': 'example/webapi/logs/app.log',
                'keys': ['created', 'filename', 'lineno', 'levelname', 'msg'],
            },
        },
        'i18n': {
            'locale': {
                'default': 'ja',
            },
            'trans': {
                'module': 'example.webapi.config.trans.{}.config',
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

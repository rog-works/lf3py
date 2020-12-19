import os


def config() -> dict:
    return {
        'env': os.environ.get('ENV', 'local'),
        'logger': {
            'dev_handler': {
                'level': 'DEBUG',
                'path': 'example/bpapi/logs/app.log',
                'keys': ['created', 'filename', 'lineno', 'levelname', 'context', 'msg'],
            },
        },
        'i18n': {
            'locale': {
                'default': 'ja',
            },
            'trans': {
                'module': 'example.bpapi.config.trans.{}.config',
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

import os


def config() -> dict:
    return {
        'env': os.environ.get('ENV', 'local'),
        'logger': {
            'dev_handler': {
                'level': 'DEBUG',
                'path': 'example/webapi/logs/app.log',
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
                'path': 'example.webapi.config.trans.{}',
                'module': 'config',
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

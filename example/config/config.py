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
            },
        },
        'response': {
            'module': os.environ.get('RESPONSE_MODULE', 'dev_response'),
            'modules': {
                'dev_response': {
                    'headers': {'Content-Type': 'application/json'},
                },
                'prd_response': {
                    'headers': {'Content-Type': 'application/json'},
                },
            },
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
    }

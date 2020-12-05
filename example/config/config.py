from os import environ


config = {
    'env': environ.get('ENV', 'local'),
    'logger': {
        'module': environ.get('LOGGER_MODULE', 'file_handler'),
        'modules': {
            'file_handler': {
                'level': environ.get('LOGGER_LEVEL', 'DEBUG'),
                'path': 'example/logs/app.log',
                'format': '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
            },
        },
    },
    'response': {
        'module': environ.get('RESPONSE_MODULE', 'dev_response'),
        'modules': {
            'dev_response': {
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

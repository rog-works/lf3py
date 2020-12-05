from os import environ


config = {
    'env': environ.get('ENV', 'local'),
    'logger': {
        'level': environ.get('LOGGER_LEVEL', 'debug'),
        'module': environ.get('LOGGER_MODULE', 'file_handler'),
        'modules': {
            'file_handler': {
                'path': environ.get('LOGGER_MODULES_FILE_HANDLER_PATH', 'example/logs/app.log'),
            },
        },
    },
    'response': {
        'headers': {
            'Content-Type': 'application/json',
        },
        'module': environ.get('RESPONSE_MODULE', 'dev_response'),
        'modules': {
            'dev_response': {},
            'prd_response': {},
        },
    },
}

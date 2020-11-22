import os


__base = {
    'env': 'local',
    'log_level': 'debug',
}

config = {key: os.environ.get(key.upper(), value) for key, value in __base.items()}

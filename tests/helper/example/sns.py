from lf3py.lang.module import load_module_path, unload_module


def perform_api(event: dict) -> dict:
    handler = load_module_path('example.sns.handler.handler')

    try:
        result = handler(event, object())
        unload_module('example.sns.handler')
        return result
    except Exception:
        unload_module('example.sns.handler')
        raise

from lf3py.lang.module import load_module_path, unload_module


def perform_api(event: dict) -> dict:
    handler = load_module_path('example.flowapi.handler.handler')

    try:
        result = handler(event, object())
        unload_module('example.flowapi.handler')
        return result
    except Exception:
        unload_module('example.flowapi.handler')
        raise

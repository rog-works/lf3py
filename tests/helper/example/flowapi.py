from lf2.lang.module import unload_module

from example.flowapi.handler import handler


def perform_api(event: dict) -> dict:
    result = handler(event, object())
    unload_module('example.flowapi.handler')
    return result

from lf2.lang.module import unload_module

from example.simple.handler import handler


def perform_api(event: dict) -> dict:
    result = handler(event, object())
    unload_module('example.simple.handler')
    return result

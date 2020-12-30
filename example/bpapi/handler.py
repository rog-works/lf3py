import example.bpapi.preprocess  # noqa: F401

from example.bpapi.app import MyApp


def handler(event: dict, context: object) -> dict:
    app = MyApp.entry(event)
    try:
        return app.run().serialize()
    except Exception as e:
        return app.render.fail(e).json().serialize()

import example.preprocess  # noqa: F401

from example.provider.aws_app import aws_app


def handler(event: dict, context: object) -> dict:
    app = aws_app(event, context)
    try:
        return app.run().serialize()
    except Exception as e:
        return app.api.error_500(e).serialize()

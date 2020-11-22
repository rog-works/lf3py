from example.provider import aws_app


def handler(event: dict, context: object) -> dict:
    app = aws_app(event, context)
    return app.run().encode()

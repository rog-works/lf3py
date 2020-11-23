from example.provider import aws_app


def handler(event: dict, context: object) -> dict:
    app = aws_app(event, context)
    try:
        return app.run().serialize()
    except Exception as e:
        return app.error_500(e).serialize()

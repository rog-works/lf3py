from example.provider import aws_app
from framework.task.runner import Runner


def handler(event: dict, context: object) -> dict:
    app = aws_app(event, context)
    try:
        return app.perform(Runner).serialize()
    except Exception as e:
        return app.api.error_500(e).serialize()

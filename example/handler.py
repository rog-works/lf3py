from framework.task.runner import Runner

from example.provider.app import aws_app


def handler(event: dict, context: object) -> dict:
    app = aws_app(event, context)
    try:
        return app.perform(Runner).serialize()
    except Exception as e:
        return app.api.error_500(e).serialize()

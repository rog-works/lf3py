from framework.api.data import Response
from framework.app import App

app = App.get()


def action() -> Response:
    return app.api.success({'success': True})

from framework.http.data import Response
from framework.app import App

app = App.get(__name__)


def action() -> Response:
    return app.api.success({'success': True})

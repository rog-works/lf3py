from framework.app import App
from framework.http.data import Response

app = App.get(__name__)


def action() -> Response:
    return app.api.success({'success': True})

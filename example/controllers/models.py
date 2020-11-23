from framework.http.data import Response
from framework.app import App

app = App.get(__name__)


def run() -> Response:
    return app.success({'success': True})

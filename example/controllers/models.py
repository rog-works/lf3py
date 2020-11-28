import re

from framework.api.data import Response
from framework.app import App

app = App.get()


def index() -> Response:
    return app.api.success({'success': True})


def show() -> Response:
    model_id = int(re.search(r'(\d+)$', app.api.request.path).group(1))
    return app.api.success({'success': True, 'id': model_id})

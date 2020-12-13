from lf2.api.data import MessageBody, Result
from lf2.api.presenter import ApiErrorPresenter


class SafeApiErrorPresenter(ApiErrorPresenter):
    def _build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return MessageBody(message=message)

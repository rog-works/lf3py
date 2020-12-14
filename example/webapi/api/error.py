from lf2.api.data import MessageBody, Result
from lf2.api.render import ApiRender


class SafeApiRender(ApiRender):
    def build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return MessageBody(message=message)

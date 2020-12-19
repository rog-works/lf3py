from lf3py.api.render import ApiRender
from lf3py.api.response import MessageBody
from lf3py.task.result import Result


class SafeApiRender(ApiRender):
    def build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return MessageBody(message=message)

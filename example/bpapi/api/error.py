from lf2.api.render import ApiRender
from lf2.api.response import MessageBody
from lf2.task.result import Result


class SafeApiRender(ApiRender):
    def build_error_body(self, status: int, message: str, error: Exception) -> Result:
        return MessageBody(message=message)

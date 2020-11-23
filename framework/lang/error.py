import traceback
from typing import List


def stacktrace(error: Exception) -> List[str]:
    return traceback.format_exception(type(error), error, error.__traceback__)

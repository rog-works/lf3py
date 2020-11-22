import traceback
from typing import List


def stacktrace(error: Exception) -> List[str]:
    return traceback.format_tb(error.__traceback__)

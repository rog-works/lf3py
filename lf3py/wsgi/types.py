from typing_extensions import Protocol
from typing import Any, Callable, List, Optional, Tuple


class StartResponse(Protocol):
    def __call__(self, status: str, headers: List[Tuple[str, str]], exc_info: Optional[Any] = ...) -> Callable[[bytes], Any]:
        ...

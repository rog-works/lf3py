from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Request:
    method: str = ''
    path: str = ''
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)

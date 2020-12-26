from dataclasses import dataclass, field
from typing import List


@dataclass
class CorsSetting:
    allow_origin: str = '*'
    allow_methods: List[str] = field(default_factory=lambda: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTION'])
    allow_headers: List[str] = field(default_factory=lambda: ['Accept', 'Content-Type'])
    max_age: int = 86400

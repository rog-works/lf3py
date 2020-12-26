from dataclasses import dataclass, field
from typing import List


@dataclass
class CorsSetting:
    allow_origin: str = ''
    allow_methods: List[str] = field(default_factory=list)
    allow_headers: List[str] = field(default_factory=list)
    max_age: str = ''

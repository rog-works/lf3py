from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SNSMessage:
    message: str = ''
    attributes: Dict[str, Dict[str, str]] = field(default_factory=dict)

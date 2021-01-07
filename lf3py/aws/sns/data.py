from dataclasses import dataclass, field
from typing import Dict

from lf3py.serialization.deserializer import DictDeserializer


@dataclass
class SNSMessage(DictDeserializer):
    message: str = ''
    attributes: Dict[str, Dict[str, str]] = field(default_factory=dict)

from dataclasses import dataclass, field
from typing import Dict

from lf3py.task.data import Result


@dataclass
class PingRecord(Result):
    topic: str = ''
    subject: str = ''
    message: str = ''


@dataclass
class NoticeRecord(Result):
    topic: str = ''
    subject: str = ''
    message: str = ''
    values: Dict[str, str] = field(default_factory=dict)

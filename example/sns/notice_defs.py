from dataclasses import dataclass, field
from typing import Dict

from lf3py.task.data import Result


@dataclass
class NoticeAttribute:
    key: str = ''
    value: str = ''


@dataclass
class NoticeMessage:
    text: str = ''
    attributes: Dict[str, NoticeAttribute] = field(default_factory=dict)


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
    attributes: Dict[str, NoticeAttribute] = field(default_factory=dict)

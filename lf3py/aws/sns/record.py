from dataclasses import dataclass, field
from typing import Dict, Type

from lf3py.lang.dsn import DSN
from lf3py.serialization.deserializer import DictDeserializer
from lf3py.task.data import Command, _T


@dataclass
class SNSRecord(Command):
    topic: str = ''
    subject: str = ''
    message: str = ''
    attributes: Dict[str, dict] = field(default_factory=dict)

    @classmethod
    def deserialize(cls, record: dict) -> 'SNSRecord':
        return cls(
            topic=record['TopicArn'].split(':')[-1:],
            subject=record['Subject'],
            message=record['Message'],
            attributes=record['MessageAttributes'],
        )

    @property
    def dsn(self) -> DSN:
        return DSN(self.topic, self.subject)

    def data(self, data_type: Type[_T]) -> _T:
        return DictDeserializer().deserialize(data_type, self.attributes)

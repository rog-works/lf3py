from dataclasses import dataclass, field
from typing import List, Type

from lf3py.lang.dsn import DSN
from lf3py.serialization.deserializer import DictDeserializer
from lf3py.task.data import Command, T_OBJ


@dataclass
class SNSRecord(Command):
    record: dict = field(default_factory=dict)

    @property
    def dsn(self) -> DSN:
        return DSN(self.record['topic'], self.record['subject'])

    def data(self, data_type: Type[T_OBJ]) -> T_OBJ:
        return DictDeserializer().deserialize(data_type, self.record)


SNSRecords = List[SNSRecord]

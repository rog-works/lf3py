from dataclasses import dataclass, field
from typing import Any, Dict, Type

from lf3py.api.dsn import ApiDSN
from lf3py.serialization.deserializer import DictDeserializer
from lf3py.task.data import Command, T_OBJ


@dataclass
class Request(Command):
    method: str = ''
    path: str = ''
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)

    @property
    def dsn(self) -> ApiDSN:
        return ApiDSN(self.method, self.path)

    def data(self, data_type: Type[T_OBJ]) -> T_OBJ:
        return DictDeserializer().deserialize(data_type, self.params)

import re
from typing import Dict, Type, Union

DSNElement = Union[int, str]


class DSN:
    @classmethod
    def format(cls, *elems: DSNElement) -> str:
        return '.'.join([str(elem) for elem in elems])

    def __init__(self, *elems: DSNElement) -> None:
        self._dsn = self.format(*elems)

    def __str__(self) -> str:
        return self._dsn

    def contains(self, spec: str) -> bool:
        return re.search(f'^{spec}$', self._dsn) is not None

    def capture(self, spec: str) -> Dict[str, str]:
        return re.search(spec, self._dsn).groupdict()

    def to_str(self) -> str:
        return str(self)


DSNType = Type[DSN]

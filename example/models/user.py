from dataclasses import dataclass
from typing import List


@dataclass
class User:
    id: int = 0
    name: str = ''

    @classmethod
    def create(cls, name: str) -> 'User':
        return cls(id=1, name=name)

    @classmethod
    def find_all(cls) -> List['User']:
        return []

    @classmethod
    def find(cls, id: int) -> 'User':
        return cls(id=id, name='hoge')

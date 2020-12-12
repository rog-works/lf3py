from dataclasses import dataclass
from typing import List

from example.webapi.repos.user_repo import UserRepo


@dataclass
class User:
    id: int = 0
    name: str = ''

    @classmethod
    def create(cls, name: str) -> 'User':
        tobj = UserRepo.create(name=name)
        return cls(**tobj)

    @classmethod
    def find_all(cls) -> List['User']:
        return [cls(**tobj) for tobj in UserRepo.find_all()]

    @classmethod
    def find(cls, id: int) -> 'User':
        tobj = UserRepo.find(id)
        return cls(**tobj)

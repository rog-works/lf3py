from dataclasses import dataclass, field
from typing import List

from lf3py.task.data import Result

from example.bpapi.models.user import User


@dataclass
class IndexBody(Result):
    success: bool = True
    users: List[User] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    success: bool = True
    user: User = field(default_factory=User)


@dataclass
class CreateParams:
    name: str = ''

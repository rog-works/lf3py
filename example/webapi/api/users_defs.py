from dataclasses import dataclass, field
from typing import List

from lf2.task.result import Result

from example.webapi.models.user import User


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

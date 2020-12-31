from dataclasses import dataclass, field
from typing import List

from lf3py.task.data import Result


@dataclass
class Model:
    id: int = 0


@dataclass
class IndexBody(Result):
    models: List[Model] = field(default_factory=list)


@dataclass
class ShowBody(Result):
    model: Model = Model()

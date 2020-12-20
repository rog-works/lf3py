from itertools import chain
from typing import Sequence, TypeVar

_T = TypeVar('_T')


flatten = chain.from_iterable


def first(iter: Sequence[_T]) -> _T:
    return iter[0]


def last(iter: Sequence[_T]) -> _T:
    return iter[-1]

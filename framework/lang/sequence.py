from itertools import chain
from typing import TypeVar, Sequence

T = TypeVar('T')


flatten = chain.from_iterable


def first(iter: Sequence[T]) -> T:
    return iter[0]


def last(iter: Sequence[T]) -> T:
    return iter[-1]

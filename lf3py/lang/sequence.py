from itertools import chain
from typing import KeysView, Iterator, Sequence, TypeVar, Union, ValuesView

_T = TypeVar('_T')


flatten = chain.from_iterable


def first(iter: Union[Sequence[_T], Iterator[_T], KeysView[_T], ValuesView[_T]]) -> _T:
    return list(iter)[0]


def last(iter: Union[Sequence[_T], Iterator[_T], KeysView[_T], ValuesView[_T]]) -> _T:
    return list(iter)[-1]

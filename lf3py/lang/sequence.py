from itertools import chain
from typing import KeysView, Iterator, Sequence, TypeVar, Union, ValuesView

T_VAL = TypeVar('T_VAL')


flatten = chain.from_iterable


def first(iter: Union[Sequence[T_VAL], Iterator[T_VAL], KeysView[T_VAL], ValuesView[T_VAL]]) -> T_VAL:
    return list(iter)[0]


def last(iter: Union[Sequence[T_VAL], Iterator[T_VAL], KeysView[T_VAL], ValuesView[T_VAL]]) -> T_VAL:
    return list(iter)[-1]

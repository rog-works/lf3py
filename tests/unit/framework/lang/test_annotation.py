from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Dict, Optional, Union
from unittest import TestCase

from framework.lang.annotation import ClassAnnotation, FunctionAnnotation
from framework.test.helper import data_provider


class EnumA(IntEnum):
    A = 1
    B = 2
    C = 3


class EnumB(Enum):
    A = 'a'
    B = 'b'
    C = 'c'


@dataclass
class AnnoA:
    a: int = 0
    b: str = ''
    c: Optional[int] = None
    d: dict = field(default_factory=dict)
    e: list = field(default_factory=list)
    f: EnumA = EnumA.A
    g: EnumB = EnumB.A

    def method_a(self, a: int, *args, b: str, **kwargs) -> Optional[int]:
        return None


def func_a(a: int, *args, b: str, **kwargs) -> int:
    return 1


class TestAnnotation(TestCase):
    def test_class(self):
        anno = ClassAnnotation(AnnoA)
        self.assertEqual(anno.origin, AnnoA)
        self.assertEqual(anno.properties['a'].origin, int)
        self.assertEqual(anno.properties['b'].origin, str)
        self.assertEqual(anno.properties['c'].origin, Union)
        self.assertEqual(anno.properties['d'].origin, dict)
        self.assertEqual(anno.properties['e'].origin, list)
        self.assertEqual(anno.properties['f'].origin, EnumA)
        self.assertEqual(anno.properties['g'].origin, EnumB)
        self.assertEqual(anno.constructor.args['a'].origin, int)
        self.assertEqual(anno.constructor.args['b'].origin, str)
        self.assertEqual(anno.constructor.args['c'].origin, Union)
        self.assertEqual(anno.constructor.args['d'].origin, dict)
        self.assertEqual(anno.constructor.args['e'].origin, list)
        self.assertEqual(anno.constructor.args['f'].origin, EnumA)
        self.assertEqual(anno.constructor.args['g'].origin, EnumB)

    def test_function(self):
        anno = FunctionAnnotation(func_a)
        self.assertEqual(anno.args['a'].origin, int)
        self.assertEqual(anno.args['b'].origin, str)
        self.assertEqual(anno.returns.origin, int)
        self.assertEqual(anno.is_method, False)

    def test_method(self):
        obj = AnnoA()
        anno = FunctionAnnotation(obj.method_a)
        self.assertEqual(anno.args['a'].origin, int)
        self.assertEqual(anno.args['b'].origin, str)
        self.assertEqual(anno.returns.origin, Union)
        self.assertEqual(anno.is_method, True)

    @data_provider([
        ('a', {'is_enum': False, 'is_union': False, 'is_optional': False}),
        ('b', {'is_enum': False, 'is_union': False, 'is_optional': False}),
        ('c', {'is_enum': False, 'is_union': True, 'is_optional': True}),
        ('d', {'is_enum': False, 'is_union': False, 'is_optional': False}),
        ('e', {'is_enum': False, 'is_union': False, 'is_optional': False}),
        ('f', {'is_enum': True, 'is_union': False, 'is_optional': False}),
        ('g', {'is_enum': True, 'is_union': False, 'is_optional': False}),
    ])
    def test_value(self, key: str, expected_data: Dict[str, bool]):
        anno = ClassAnnotation(AnnoA)
        anno_props = anno.properties
        for method_key, expected in expected_data.items():
            actual = getattr(anno_props[key], method_key)
            self.assertEqual(actual, expected)

from unittest import TestCase

from lf3py.lang.cache import Cache, Storage


class TestCache(TestCase):
    def test_cache(self):
        storage = Storage()
        cache = Cache(storage)

        @cache(inject_keys=lambda: [2, 'piyo'])
        def fetch(a: int, b: str) -> str:
            return f'{a}+{b}'

        expected_key = f'{__name__}.fetch.2.piyo.1.hoge'
        self.assertEqual(fetch(1, 'hoge'), '1+hoge')
        self.assertEqual(storage.get(expected_key), '1+hoge')

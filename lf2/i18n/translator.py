from typing import cast

from lf2.lang.dict import pluck


class Translator:
    def __init__(self, config: dict) -> None:
        self._config = config

    def trans(self, path: str) -> str:
        return cast(str, pluck(self._config, path))

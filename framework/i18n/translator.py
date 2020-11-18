from typing import cast


from framework.data.config import TransConfig
from framework.lang.dict import pluck


class Translator:
    def __init__(self, config: TransConfig) -> None:
        self._config: dict = config

    def trans(self, path: str) -> str:
        return cast(str, pluck(self._config, path))

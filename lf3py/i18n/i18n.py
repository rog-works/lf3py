from datetime import tzinfo

from lf3py.i18n.datetime import DateTime
from lf3py.i18n.translator import Translator


class I18n:
    def __init__(self, tzinfo: tzinfo, trans_config: dict) -> None:
        self._datetime = DateTime(tzinfo)
        self._translator = Translator(trans_config)

    @property
    def datetime(self) -> DateTime:
        return self._datetime

    def trans(self, path: str) -> str:
        return self._translator.trans(path)

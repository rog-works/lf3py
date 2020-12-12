from lf2.i18n.datetime import DateTime
from lf2.i18n.tzinfo import TZInfo
from lf2.i18n.translator import Translator


class I18n:
    def __init__(self, tzinfo: TZInfo, trans_config: dict) -> None:
        self._datetime = DateTime(tzinfo)
        self._translator = Translator(trans_config)

    def datetime(self) -> DateTime:
        return self._datetime

    def trans(self, path: str) -> str:
        return self._translator.trans(path)

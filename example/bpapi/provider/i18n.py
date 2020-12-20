from typing import cast

from lf3py.api.request import Request
from lf3py.config import Config
from lf3py.i18n.i18n import I18n
from lf3py.i18n.tzinfo import TZInfo
from lf3py.lang.module import load_module_path
from lf3py.task.data import Command


def make_i18n(config: Config, command: Command) -> I18n:
    request = cast(Request, command)  # XXX remove cast
    locale = request.params.get('locale', config['i18n']['locale']['default'])
    trans_config = load_module_path(config["i18n"]["trans"]["module"].format(locale))
    return I18n(to_tzinfo(locale), trans_config)


def to_tzinfo(locale: str) -> TZInfo:
    defs = {
        'ja': {'hours': 9, 'dst': 0, 'tzname': 'Asia/Tokyo'},
    }
    return TZInfo(**defs[locale])

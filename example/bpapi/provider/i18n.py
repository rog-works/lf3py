from lf3py.api.request import Request
from lf3py.data.config import Config
from lf3py.i18n.i18n import I18n
from lf3py.i18n.tzinfo import TZInfo
from lf3py.lang.module import load_module_path


def make_i18n(config: Config, request: Request) -> I18n:
    locale: str = request.params.get('locale', config['i18n']['locale']['default'])
    trans_config: dict = load_module_path(config["i18n"]["trans"]["module"].format(locale))
    return I18n(to_tzinfo(locale), trans_config)


def to_tzinfo(locale: str) -> TZInfo:
    defs = {
        'ja': {'hours': 9, 'dst': 0, 'tzname': 'Asia/Tokyo'},
    }
    return TZInfo(**defs[locale])

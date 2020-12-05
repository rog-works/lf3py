from framework.api.data import Request
from framework.data.config import Config
from framework.i18n.i18n import I18n
from framework.i18n.tzinfo import TZInfo
from framework.lang.module import load_module


def make_i18n(config: Config, request: Request) -> I18n:
    locale: str = request.params.get('locale', config['i18n']['locale']['default'])
    trans_config: dict = load_module(
        config["i18n"]["trans"]["path"].format(locale),
        config['i18n']['trans']['module']
    )
    return I18n(to_tzinfo(locale), trans_config)


def to_tzinfo(locale: str) -> TZInfo:
    defs = {
        'ja': {'hours': 9, 'dst': 0, 'tzname': 'Asia/Tokyo'},
    }
    return TZInfo(**defs[locale])

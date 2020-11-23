from framework.i18n.i18n import I18n
from framework.http.data import Request
from framework.lang.module import load_module


def make_i18n(request: Request) -> I18n:
    locale: str = request.params.get('locale', 'ja')
    trans_config: dict = load_module(f'example.trans.{locale}', 'config')
    return I18n(locale, trans_config)

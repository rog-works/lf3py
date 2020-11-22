from framework.i18n.locale import Locale
from framework.data.http import Request
from framework.lang.module import load_module


def make_locale(request: Request) -> Locale:
    locale: str = request.params.get('locale', 'ja')
    trans_config: dict = load_module(f'example.trans.{locale}', 'config')
    return Locale(locale, trans_config)

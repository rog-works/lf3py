from typing import Tuple

from lf3py.app.app import App
from lf3py.lang.module import load_module_path
from lf3py.middleware.middleware import Performer
from lf3py.routing.args import resolve_args
from lf3py.routing.symbols import IRouter
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner


def dispatch(command: Command, router: IRouter) -> Result:
    spec, module_path = router.resolve(str(command.dsn))
    runner, mw_performer = __resolve(module_path)
    try:
        mw_performer.perform()
        kwargs = resolve_args(runner, command, spec)
        return runner(**kwargs)
    except Exception as e:
        mw_performer.handle_error(e)
        raise


def __resolve(module_path: str) -> Tuple[Runner, Performer]:
    runner = load_module_path(module_path)
    bp_app = App.get(runner.__module__)
    root_app = App.get()
    return runner, bp_app.middleware.build_performer(runner, root_app.locator)

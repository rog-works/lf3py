from typing import Tuple

from lf3py.app.app import App
from lf3py.lang.module import load_module_path
from lf3py.middleware.middleware import Performer
from lf3py.routing.args import resolve_args
from lf3py.routing.router import FlowRouter
from lf3py.routing.symbols import IDispatcher, IRouter
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner


class Dispatcher(IDispatcher):
    def dispatch(self, command: Command, router: IRouter) -> Result:
        spec, runner = self._resolve_spec_runner(command, router)
        mw_performer = self._resolve_mw_performer(runner)
        try:
            mw_performer.perform()
            kwargs = resolve_args(runner, command, spec)
            return runner(**kwargs)
        except Exception as e:
            mw_performer.handle_error(e)
            raise

    def _resolve_spec_runner(self, command: Command, router: IRouter) -> Tuple[str, Runner]:
        raise NotImplementedError()

    def _resolve_mw_performer(self, runner: Runner) -> Performer:
        raise NotImplementedError()


class BpDispatcher(Dispatcher):
    def _resolve_spec_runner(self, command: Command, router: IRouter) -> Tuple[str, Runner]:
        spec, module_path = router.resolve(str(command.dsn))
        return spec, load_module_path(module_path)

    def _resolve_mw_performer(self, runner: Runner) -> Performer:
        bp_app = App.get(runner.__module__)
        root_app = App.get()
        return bp_app.middleware.build_performer(runner, root_app.locator)


class FlowDispatcher(Dispatcher):
    def _resolve_spec_runner(self, command: Command, router: FlowRouter) -> Tuple[str, Runner]:
        return router.resolve_runner(str(command.dsn))

    def _resolve_mw_performer(self, runner: Runner) -> Performer:
        root_app = App.get()
        return root_app.middleware.build_performer(runner, root_app.locator)

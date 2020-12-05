from framework.lang.module import load_module
from framework.data.config import Config
from framework.api.data import Response


def make_response(config: Config) -> Response:
    func_name = config['response']['module']
    func_args = config['response']['modules'][func_name]
    return load_module(__name__, func_name)(**func_args)


def dev_response(headers: dict) -> Response:
    return Response(headers=headers)

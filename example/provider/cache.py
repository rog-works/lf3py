from framework.lang.cache import Cache, Storage
from framework.data.config import Config
from framework.lang.module import load_module


def make_cache(config: Config) -> Cache:
    func_name = config['cache']['module']
    func_args = config['cache']['module'][func_name]
    return load_module(__name__, func_name)(**func_args)


def dev_cache() -> Cache:
    return Cache(Storage())

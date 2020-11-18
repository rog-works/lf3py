from typing import Callable, List, Tuple


def data_provider(args_list: List[Tuple]):
    def decorator(test_func: Callable):
        def wrapper(self, *_):
            for provide_args in args_list:
                test_func(self, *provide_args)

        return wrapper

    return decorator

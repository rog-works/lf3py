from typing import Callable, List, Optional, TypeVar, Union

_T = TypeVar('_T')
ContextInjector = Callable[[], List[Union[int, str]]]


class Storage(dict):
    pass


class Cache:
    def __init__(self, storage: Storage = Storage()) -> None:
        self._storage = storage

    def __call__(self, inject_keys: Optional[ContextInjector] = None) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
        """
        Examples:
            >>> @app.cache(inject_keys=lambda: [self.id])
            >>> def get_slow_content(self, cached: bool) -> dict:
            >>>     return requests.get(f'https://example.com/models/{self.id}/content').json()
        """
        def decorator(wrapper_func: Callable[..., _T]) -> Callable[..., _T]:
            def wrapper(*args, **kwargs) -> _T:
                context = inject_keys() if inject_keys is not None else []
                cache_key = self.__calc_cache_key(wrapper_func, context, *args, **kwargs)
                force = 'cached' in kwargs and not kwargs['cached']
                if cache_key not in self._storage or force:
                    self._storage[cache_key] = wrapper_func(*args, **kwargs)

                return self._storage[cache_key]

            return wrapper

        return decorator

    def __calc_cache_key(self, func: Callable, context: List[Union[int, str]], *args, **kwargs) -> str:
        return '.'.join([
            *[func.__module__, func.__name__],
            *[str(elem) for elem in context],
            *[str(elem) for elem in args],
            *[str(elem) for elem in kwargs.values()],
        ])

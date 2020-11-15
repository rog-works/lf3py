from typing import Any, Callable, Dict, Type


Factory = Callable[[], Any]


class DI:
    def __init__(self) -> None:
        self._factories: Dict[Type, Factory] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, klass: Type, factory: Factory):
        self._factories[klass] = factory

    def resolve(self, klass: Type) -> Any:
        if klass not in self._factories:
            raise ValueError()

        if klass in self._instances:
            return self._instances[klass]

        factory = self._factories[klass]
        instance = factory()
        self._instances[klass] = instance
        return instance

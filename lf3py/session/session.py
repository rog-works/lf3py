from typing import Any, Dict


class Session:
    __contexts: Dict[str, Any] = {}

    @classmethod
    def add_context(cls, name: str, context: Any):
        cls.__contexts[name] = context

    @classmethod
    def context(cls, name: str) -> Any:
        return cls.__contexts[name]

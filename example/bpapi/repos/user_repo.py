from typing import List


class UserRepo:
    @classmethod
    def create(cls, name: str) -> dict:
        raise NotImplementedError()

    @classmethod
    def find_all(cls) -> List[dict]:
        raise NotImplementedError()

    @classmethod
    def find(cls, id: int) -> dict:
        raise NotImplementedError()

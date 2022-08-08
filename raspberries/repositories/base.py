import abc
from typing import List

from raspberries.entities.models import Base


class AbstractRepository(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def add(data: Base) -> Base:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    async def merge(data: Base) -> Base:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    async def get(ids: str | List[str]) -> Base | List[Base]:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    async def delete(ids: str | List[str]) -> None:
        raise NotImplementedError

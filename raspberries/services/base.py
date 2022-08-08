import abc
from typing import Dict, List, Type

from raspberries.adapters.dto import GenericCreateDto, GenericUpdateDto
from raspberries.entities.models import Base
from raspberries.repositories.base import AbstractRepository

SUPPORTED_SERVICES = dict()


class AbstractService(abc.ABC):
    repository: AbstractRepository
    service_id: str

    @abc.abstractmethod
    async def create(self, data: GenericCreateDto) -> Base:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, data: GenericUpdateDto) -> Base:
        raise NotImplementedError

    @abc.abstractmethod
    async def retrieve(self, ids: str | List[str]) -> Base | List[Base]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, ids: str | List[str]) -> None:
        raise NotImplementedError


def service(service_type: Type[AbstractService]) -> Type[AbstractService]:
    service_instance = service_type()
    service_id = service_instance.service_id
    SUPPORTED_SERVICES[service_id] = service_instance
    return service_type


def get_service(service_id: str) -> AbstractService:
    try:
        return SUPPORTED_SERVICES[service_id]
    except KeyError:
        raise KeyError(f"'{service_id}' service is not provided")

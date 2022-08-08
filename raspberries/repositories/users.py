from typing import List

from sqlalchemy.future import select

from raspberries.adapters.db import async_session
from raspberries.entities.models import User
from raspberries.repositories.base import AbstractRepository


class UserRepository(AbstractRepository):
    @staticmethod
    async def add(data: User) -> User:
        async with async_session() as session:
            await session.add(data)
            await session.commit()

        return data

    @staticmethod
    async def merge(data: User) -> User:
        async with async_session() as session:
            await session.merge(data)
            await session.commit()

        return data

    @staticmethod
    async def get(ids: str | List[str]) -> User | List[User]:
        query = select(User).where(User.id.in_(ids))
        async with async_session() as session:
            results = await session.execute(query)
            return results.scalars()

    @staticmethod
    async def delete(ids: str | List[str]) -> None:
        query = select(User).where(User.id.in_(ids))
        async with async_session() as session:
            results = await session.execute(query)
            await session.delete(results)
            await session.commit()

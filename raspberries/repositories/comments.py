from typing import List

from sqlalchemy.future import select

from raspberries.adapters.db import async_session
from raspberries.entities.models import Comment
from raspberries.repositories.base import AbstractRepository


class CommentRepository(AbstractRepository):
    @staticmethod
    async def add(data: Comment) -> Comment:
        async with async_session() as session:
            await session.add(data)
            await session.commit()

        return data

    @staticmethod
    async def merge(data: Comment) -> Comment:
        async with async_session() as session:
            await session.merge(data)
            await session.commit()

        return data

    @staticmethod
    async def get(ids: str | List[str]) -> Comment | List[Comment]:
        query = select(Comment).where(Comment.id.in_(ids))
        async with async_session() as session:
            results = await session.execute(query)
            return results.scalars()

    @staticmethod
    async def delete(ids: str | List[str]) -> None:
        query = select(Comment).where(Comment.id.in_(ids))
        async with async_session() as session:
            results = await session.execute(query)
            await session.delete(results)
            await session.commit()

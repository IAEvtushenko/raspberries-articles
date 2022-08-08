from typing import List

from raspberries.adapters.dto import CommentCreateDto, CommentUpdateDto
from raspberries.entities.models import Article
from raspberries.repositories.comments import CommentRepository
from raspberries.services.base import service, AbstractService


@service
class CommentService(AbstractService):
    repository = CommentRepository
    service_id = "comment"

    @classmethod
    async def create(cls, data: CommentCreateDto) -> Article:
        article = Article(data.dict())
        return await cls.repository.add(article)

    @classmethod
    async def update(cls, data: CommentUpdateDto) -> Article:
        return await cls.repository.merge(Article(data.dict()))

    @classmethod
    async def retrieve(cls, ids: str | List[str]) -> Article | List[Article]:
        return await cls.repository.get(ids)

    @classmethod
    async def delete(cls, ids: str | List[str]) -> None:
        await cls.repository.delete(ids)

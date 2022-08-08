from typing import List

from raspberries.adapters.dto import ArticleCreateDto, ArticleUpdateDto
from raspberries.entities.models import Article
from raspberries.repositories.articles import ArticleRepository
from raspberries.services.base import service, AbstractService


@service
class ArticleService(AbstractService):
    repository = ArticleRepository
    service_id = "article"

    @classmethod
    async def create(cls, data: ArticleCreateDto) -> Article:
        article = Article(data.dict())
        return await cls.repository.add(article)

    @classmethod
    async def update(cls, data: ArticleUpdateDto) -> Article:
        return await cls.repository.merge(Article(data.dict()))

    @classmethod
    async def retrieve(cls, ids: str | List[str]) -> Article | List[Article]:
        return await cls.repository.get(ids)

    @classmethod
    async def delete(cls, ids: str | List[str]) -> None:
        await cls.repository.delete(ids)

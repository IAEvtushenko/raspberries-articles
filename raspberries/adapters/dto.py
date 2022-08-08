from typing import Optional, List
from pydantic import BaseModel, validator

from raspberries.adapters.validators import is_password_valid


class GenericCreateDto(BaseModel):
    pass


class GenericUpdateDto(BaseModel):
    pass


class GenericRetrieveDeleteDto(BaseModel):
    ids: str | List[str]


class UserCreateDto(GenericCreateDto):
    username: str
    password: str

    @validator("password")
    def validate_password(self, value):
        is_password_valid(value)
        return value


class UserUpdateDto(GenericUpdateDto):
    id: int
    username: str


class ArticleCreateDto(GenericCreateDto):
    title: str
    content: str
    author_id: str


class ArticleUpdateDto(GenericUpdateDto):
    id: str
    title: Optional[str]
    content: Optional[str]


class CommentCreateDto(GenericCreateDto):
    content: str
    author_id: str
    article_id: str
    reply_to_id: Optional[str]


class CommentUpdateDto(GenericUpdateDto):
    id: str
    content: str

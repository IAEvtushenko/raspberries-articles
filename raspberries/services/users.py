from datetime import datetime, timedelta
from typing import List, Dict, Any

from jose import jwt
from passlib.context import CryptContext

from raspberries.adapters.dto import UserCreateDto, UserUpdateDto
from raspberries.entities.models import User
from raspberries.repositories.users import UserRepository
from raspberries.services.base import AbstractService, service
from raspberries.services.config import settings


@service
class UserService(AbstractService):
    repository = UserRepository
    service_id = "user"
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def create(cls, data: UserCreateDto) -> User:
        user = User(
            username=data.username,
            password=cls.get_hashed_password(data.password)
        )
        return await cls.repository.add(user)

    @classmethod
    async def update(cls, data: UserUpdateDto) -> User:
        return await cls.repository.merge(User(data.dict()))

    @classmethod
    async def retrieve(cls, ids: str | List[str]) -> User | List[User]:
        return await cls.repository.get(ids)

    @classmethod
    async def delete(cls, ids: str | List[str]) -> None:
        await cls.repository.delete(ids)

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_pass: str) -> bool:
        return cls.password_context.verify(password, hashed_pass)

    @staticmethod
    def create_access_token(subject: Any, expire_delta: int = None) -> str:
        ttl_minutes = expire_delta if expire_delta else settings.refresh_token_expire_minutes
        expire_time = datetime.utcnow() + timedelta(minutes=ttl_minutes)

        to_encode = {"exp": expire_time, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)

        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Any, expire_delta: int = None) -> str:
        ttl_minutes = expire_delta if expire_delta else settings.refresh_token_expire_minutes
        expire_time = datetime.utcnow() + timedelta(minutes=ttl_minutes)

        to_encode = {"exp": expire_time, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, settings.jwt_algorithm)

        return encoded_jwt

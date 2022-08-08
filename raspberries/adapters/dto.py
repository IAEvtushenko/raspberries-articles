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
    username: str

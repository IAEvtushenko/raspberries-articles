import uuid

from bcrypt import hashpw, checkpw, gensalt
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, func, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base, backref

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    _password = Column(String(16))
    articles = relationship(
        "Article",
        backref="author",
        cascade="all, delete"
    )

    @hybrid_property
    def password(self):
        return self._password

    def _set_password(self, password: str):
        self._password = password

    def init(self, username, password):
        self.username = username
        self._set_password(password)


class Article(Base):
    __tablename__ = "article"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String(128))
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(
        "User",
        backref=backref("articles")
    )


class Comment(Base):
    __tablename__ = "comment"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(
        "User",
        backref=backref(
            "comments",
            cascade="all, delete"
        )
    )


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    departments = relationship(
        "Department",
        backref="company"
    )
    employees = relationship(
        "Employee",
        backref="company"
    )

    @property
    def size(self):
        return len(self.employees)


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship(
        "Company",
        backref="departments"
    )
    employees = relationship(
        "Employee",
        backref="department"
    )

    @property
    def size(self):
        return len(self.employees)


class Employee(Base):
    __tablename__ = "employee"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    full_name = Column(String(128))
    role = Column(String(32))
    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship(
        "Company",
        backref="employees"
    )
    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship(
        "Department",
        backref="employees"
    )
    hired_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    salary = Column(Float)
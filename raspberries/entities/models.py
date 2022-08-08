import uuid
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Text, DateTime, func
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
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

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
    comments = relationship(
        "Comment",
        backref="article",
        cascade="all, delete"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


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
    article_id = Column(UUID, ForeignKey("article.id"))
    article = relationship(
        "Article",
        backref="comments"
    )
    reply_to_id = Column(UUID, ForeignKey("comment.id"))
    replies = relationship(
        "Comment",
        backref=backref("reply_to", remote_side=[id]),
        cascade="all, delete",
        lazy="joined"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

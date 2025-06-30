from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class MediaTypeEnum(enum.Enum):
    image = "image"
    video = "video"
    audio = "audio"


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    posts = relationship("Post", back_populates="user",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan")

    followers = relationship("Follower",
                             foreign_keys='Follower.user_to_id',
                             back_populates="user_to",
                             cascade="all, delete-orphan")

    following = relationship("Follower",
                             foreign_keys='Follower.user_from_id',
                             back_populates="user_from",
                             cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,

        }


class Follower(db.Model):
    __tablename__ = 'follower'
    user_from_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), primary_key=True)

    user_from = relationship("User", foreign_keys=[
                             user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[
                           user_to_id], back_populates="followers")


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaTypeEnum] = mapped_column(
        Enum(MediaTypeEnum), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('post.id'), nullable=False)

    post = relationship("Post", back_populates="media")


class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('post.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Integer, DECIMAL, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class TypeEnum(str, Enum):
    MOVIE = 'movie'
    MUSIC = 'music'
    BOOK = 'book'


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    length: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(String(100))
    cover_image_url: Mapped[str]
    casts: Mapped[str]
    genre: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True, default=TypeEnum.MOVIE)
    thriller: Mapped[str]
    average_rating: Mapped[float] = mapped_column(Float, nullable=True)
    reviews: Mapped[list["Movie"]] = relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.title


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author: Mapped[str]
    comment: Mapped[str] = mapped_column(String(400))
    rating: Mapped[int]
    ip_address: Mapped[str] = mapped_column(String(255))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    movie = relationship(Movie, back_populates="reviews")

from decimal import Decimal
from sqlalchemy import String, Integer, DECIMAL, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    length: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(String(100))
    cover_image_url: Mapped[str]
    casts: Mapped[str]
    genre: Mapped[str]
    thriller: Mapped[str]
    reviews: Mapped[list["Movie"]] = relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.title


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author: Mapped[str]
    comment: Mapped[str]
    rating: Mapped[int]
    average_rating: Mapped[float] = mapped_column(Float)
    ip_address: Mapped[str] = mapped_column(String(255))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    movie = relationship(Movie, back_populates="reviews")

from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, DECIMAL, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.schema.movie_schema import TypeEnum

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    length: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(String(100))
    cover_image_url: Mapped[str]
    casts: Mapped[str]
    genre: Mapped[str] = mapped_column(String, nullable=True)
    item_type: Mapped[str] = mapped_column(
        String, nullable=True, default=TypeEnum.MOVIE
    )
    thriller: Mapped[str]
    average_rating: Mapped[float] = mapped_column(Float, nullable=True)
    reviews: Mapped[list["Movie"]] = relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=datetime.now()
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=datetime.now()
    )

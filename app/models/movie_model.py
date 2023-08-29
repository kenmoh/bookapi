from decimal import Decimal
from typing import List
from sqlalchemy import String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    length: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(String(100))
    cover_image_url: Mapped[str]

    casts: Mapped[List['Cast']] = relationship(back_populates='movie', cascade="all, delete-orphan")

    def __str__(self):
        return self.title


class Cast(Base):
    __tablename__ = 'casts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie: Mapped[Movie] = relationship(back_populates='casts')

    def __str__(self):
        return self.full_name

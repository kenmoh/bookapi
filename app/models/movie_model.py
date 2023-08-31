from decimal import Decimal
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    length: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.00)
    description: Mapped[str] = mapped_column(String(100))
    cover_image_url: Mapped[str]
    casts: Mapped[str]

    def get_casts_list(self):
        return self.casts.split(',')

    def __str__(self):
        return self.title




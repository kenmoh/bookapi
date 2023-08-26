from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author: Mapped[str] = mapped_column(String(75))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    isbn: Mapped[str]
    rating: Mapped[int]

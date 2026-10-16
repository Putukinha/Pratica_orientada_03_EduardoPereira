from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    books: Mapped[List["Book"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    livros: Mapped[List["Book"]] = relationship(
        back_populates="usuario",
        overlaps="books,user",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="books", overlaps="livros,usuario")
    usuario: Mapped["User"] = relationship(back_populates="livros", overlaps="books,user")


Usuario = User
Livro = Book
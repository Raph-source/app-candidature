from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base

class Admin(Base):
    __tablename__ = "admin"

    id:   Mapped[int]  = mapped_column(primary_key=True)
    nom:  Mapped[str]  = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    mdp:  Mapped[str]  = mapped_column(String(50), nullable=False)
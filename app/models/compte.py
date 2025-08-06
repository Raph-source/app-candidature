from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy import String
from .base import Base

class Compte(Base):
    __tablename__ = "compte"

    id:            Mapped[int] = mapped_column(primary_key=True)
    login:        Mapped[str] = mapped_column(String(50))
    password:    Mapped[str] = mapped_column(String(50))
    id_candidat:   Mapped[int] = mapped_column(ForeignKey("candidat.id"), nullable=False)

    candidat      = relationship("Candidat", back_populates="compte")

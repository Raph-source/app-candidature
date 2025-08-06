from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base

class Candidat(Base):
    __tablename__ = "candidat"

    id:        Mapped[int]  = mapped_column(primary_key=True)
    nom:       Mapped[str]  = mapped_column(String(50))
    lieu:       Mapped[str]  = mapped_column(String(50))
    etat_civ:       Mapped[str]  = mapped_column(String(50))
    age:       Mapped[int]
    date_naiss:  Mapped[str] = mapped_column(String(50))
    email:     Mapped[str]  = mapped_column(String(50), unique=True, nullable=False)
    nationalite:       Mapped[str]  = mapped_column(String(50), nullable=False)

    compte      = relationship("Compte", back_populates="candidat")
    cv   = relationship("Cv", back_populates="candidat", uselist=False)
    detailPostuler = relationship("DetailPostuler", back_populates="candidat")


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from .base import Base

class Dossier(Base):
    __tablename__ = "dossier"

    id:            Mapped[int] = mapped_column(primary_key=True)
    cv:            Mapped[str] = mapped_column(nullable=False)
    lettre_motivation: Mapped[str]
    diplome:       Mapped[str]
    date_depot:    Mapped[date] = mapped_column(default=date.today)
    id_candidat:   Mapped[int] = mapped_column(ForeignKey("candidat.id"), nullable=False)
    id_departement:Mapped[int] = mapped_column(ForeignKey("departement.id"), nullable=False)

    candidat      = relationship("Candidat", back_populates="dossier")
    departement      = relationship("Departement", back_populates="dossier")

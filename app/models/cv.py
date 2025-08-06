from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from datetime import date
from .base import Base

class Cv(Base):
    __tablename__ = "cv"

    id:            Mapped[int] = mapped_column(primary_key=True)
    chemin:        Mapped[str] = mapped_column(String(255))
    date_depot:    Mapped[date] = mapped_column(default=date.today)
    id_candidat:   Mapped[int] = mapped_column(ForeignKey("candidat.id"), nullable=False)
    id_poste:      Mapped[int] = mapped_column(ForeignKey("poste.id"), nullable=False)

    candidat      = relationship("Candidat", back_populates="cv")
    poste      = relationship("Poste", back_populates="cv")

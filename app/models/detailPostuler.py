from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from .base import Base

class DetailPostuler(Base):
    __tablename__ = "detailPostuler"

    id:         Mapped[int]  = mapped_column(primary_key=True)
    date_depot: Mapped[date] = mapped_column(default=date.today)
    id_candidat: Mapped[int] = mapped_column(ForeignKey("candidat.id"), nullable=False)
    id_offre:    Mapped[int] = mapped_column(ForeignKey("offre.id"), nullable=True)
    id_poste:    Mapped[int] = mapped_column(ForeignKey("poste.id"), nullable=False)

    candidat = relationship("Candidat", back_populates="detailPostuler")
    offre    = relationship("Offre", back_populates="detailPostuler")
    poste    = relationship("Poste", back_populates="detailPostuler")

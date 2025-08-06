from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from .base import Base

class Offre(Base):
    __tablename__ = "offre"

    id:          Mapped[int]  = mapped_column(primary_key=True)
    titre:       Mapped[str]  = mapped_column(String(255), nullable=False)
    description: Mapped[str]  = mapped_column(String(255), nullable=False)
    date_limite: Mapped[date]
    id_poste: Mapped[int] = mapped_column(ForeignKey("poste.id"), nullable=False)
    id_contrat: Mapped[int] = mapped_column(ForeignKey("contrat.id"), nullable=False)

    poste = relationship("Poste", back_populates="offre")
    contrat = relationship("Contrat", back_populates="offre")
    detailPostuler = relationship("DetailPostuler", back_populates="offre")

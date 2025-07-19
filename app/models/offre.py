from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from .base import Base

class Offre(Base):
    __tablename__ = "offre"

    id:          Mapped[int]  = mapped_column(primary_key=True)
    titre:       Mapped[str]  = mapped_column(String(255), nullable=False)
    description: Mapped[str]
    date_limite: Mapped[date]
    id_departement: Mapped[int] = mapped_column(ForeignKey("departement.id"), nullable=False)

    departement = relationship("Departement", back_populates="offre")
    candidature = relationship("Candidature", back_populates="offre")

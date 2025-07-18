from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base

class Departement(Base):
    __tablename__ = "departement"

    id:        Mapped[int]  = mapped_column(primary_key=True)
    nom:       Mapped[str]  = mapped_column(String(100))

    offre = relationship("Offre", back_populates="departement")
    dossier = relationship("Dossier", back_populates="departement")

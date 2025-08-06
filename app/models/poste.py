from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base

class Poste(Base):
    __tablename__ = "poste"

    id:        Mapped[int]  = mapped_column(primary_key=True)
    nom:       Mapped[str]  = mapped_column(String(100))

    offre = relationship("Offre", back_populates="poste")
    cv = relationship("Cv", back_populates="poste")
    detailPostuler = relationship("DetailPostuler", back_populates="poste")

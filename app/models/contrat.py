from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from datetime import date
from .base import Base

class Contrat(Base):
    __tablename__ = "contrat"

    id:            Mapped[int] = mapped_column(primary_key=True)
    typeContrat:        Mapped[str] = mapped_column(String(50))

    offre      = relationship("Offre", back_populates="contrat")

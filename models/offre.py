from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from datetime import date
from .base import Base

class Offre(Base):
    __tablename__ = "offre"

    id:          Mapped[int]  = mapped_column(primary_key=True)
    titre:       Mapped[str]  = mapped_column(String(50), nullable=False)
    description: Mapped[str]
    date_limite: Mapped[date]

    candidatures = relationship("Candidature", back_populates="offre")

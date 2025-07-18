from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from .base import Base

class Candidature(Base):
    __tablename__ = "candidature"

    id:         Mapped[int]  = mapped_column(primary_key=True)
    date_depot: Mapped[date] = mapped_column(default=date.today)
    status:     Mapped[bool] = mapped_column(default=False)
    id_candidat: Mapped[int] = mapped_column(ForeignKey("candidat.id"), nullable=False)
    id_offre:    Mapped[int] = mapped_column(ForeignKey("offre.id"), nullable=True)

    candidat = relationship("Candidat", back_populates="candidatures")
    offre    = relationship("Offre", back_populates="candidatures")

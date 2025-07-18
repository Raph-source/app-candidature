from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base

class Candidat(Base):
    __tablename__ = "candidat"

    id:        Mapped[int]  = mapped_column(primary_key=True)
    nom:       Mapped[str]  = mapped_column(String(50))
    post_nom:  Mapped[str]  = mapped_column(String(50))
    prenom:    Mapped[str]  = mapped_column(String(50))
    email:     Mapped[str]  = mapped_column(String(50), unique=True, nullable=False)
    mdp:       Mapped[str]  = mapped_column(String(50), nullable=False)

    dossier   = relationship("Dossier", back_populates="candidat", uselist=False)
    candidatures = relationship("Candidature", back_populates="candidat")


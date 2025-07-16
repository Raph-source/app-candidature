from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import logging
from fastapi import HTTPException
from datetime import date
from app.models.admin import Admin as Admin_M
from app.models.offre import Offre

class Admin:
    @staticmethod
    async def login(session: AsyncSession, email: str,mdp: str,) -> bool:
        """Retourne True si les identifiants sont corrects."""
        try:
            result = await session.execute(
                select(Admin_M).where(Admin_M.email == email, Admin_M.mdp == mdp)
            )
            admin = result.scalar_one_or_none()
            if not admin:
                return False
            return True
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

    async def ajouter_offre(session: AsyncSession, titre: str, description: str, date_limite: date, idDepartement: int) -> Admin_M:
        try:
            
            #ajouter le candidat
            offre = Offre(titre=titre, description=description, date_limite=date_limite, idDepartement=idDepartement)
            session.add(offre)
            await session.commit()
            await session.refresh(offre)

            return offre
        
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

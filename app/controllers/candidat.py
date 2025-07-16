from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import logging
from fastapi import HTTPException

from app.models.candidat import Candidat as Candidat_M
from app.models.departement import Departement

class Candidat:
    #création du compte
    @staticmethod
    async def sign_in(session: AsyncSession, nom: str, post_nom: str, prenom: str, email: str, mdp: str, ) -> Candidat_M:
        """retourne le Candidat si la création réeussie"""
        try:
            #Vérifier unicité e‑mail
            result = await session.execute(
                select(Candidat_M).where(Candidat_M.email == email)
            )
            if result.scalar_one_or_none():
                return False
            else:
                #ajouter le candidat
                candidat = Candidat_M(nom=nom, post_nom=post_nom, prenom=prenom, email=email, mdp=mdp,)
                session.add(candidat)
                await session.commit()
                await session.refresh(candidat)

                return candidat
        
        except Exception as e:
            print(e)
            logging.exception("Erreur interne sign_in") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

    @staticmethod
    async def login(session: AsyncSession, email: str,mdp: str,) -> bool:
        """Retourne True si les identifiants sont corrects."""
        try:
            result = await session.execute(
                select(Candidat_M).where(Candidat_M.email == email, Candidat_M.mdp == mdp)
            )
            candidat = result.scalar_one_or_none()
            if not candidat:
                return False
            return True
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    @staticmethod
    async def get_departement(session: AsyncSession):
        """retourne la liste des départements"""
        try:
            result = await session.execute(
                select(Departement)
            )
            departement = result.scalar_one_or_none()
            
            return departement
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
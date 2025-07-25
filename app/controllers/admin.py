from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging

from fastapi import HTTPException
from datetime import date

import smtplib
import ssl
from email.message import EmailMessage
import os
from app.models.admin import Admin as Admin_M
from app.models.offre import Offre
from app.models.candidature import Candidature
from app.models.departement import Departement
from app.models.dossier import Dossier
from app.models.candidat import Candidat

from app.dto.admin import AdminDTO
from app.dto.offre import OffreDTO
from app.dto.candidature import CandidatureDTO
from app.dto.candidature import CandidatureDTO
from app.dto.departement import DepartementDTO

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
            offre = Offre(titre=titre, description=description, date_limite=date_limite, id_departement=idDepartement)
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

    async def get_candidature(session: AsyncSession, id_departement: int,):
        """Retourne les candidatures"""
        try:
            stmt = (
                select(Candidature)
                .options(
                    joinedload(Candidature.candidat),
                    joinedload(Candidature.departement),
                    joinedload(Candidature.offre)
                )
                .where(Candidature.id_departement == id_departement)
                .where(Candidature.status == False)
            )
            
            result = await session.execute(stmt)
            candidatures = result.unique().scalars().all()
            return candidatures

        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def get_dossier(session: AsyncSession, id_candidat: int, id_departement: int,):
        """Retourne le dossier d'un candidat"""
        try:
            stmt = (
                select(Dossier)
                .where(Dossier.id_candidat == id_candidat)
                .where(Dossier.id_departement == id_departement)
            )
            
            result = await session.execute(stmt)
            dossier = result.unique().scalars().all()
            return dossier

        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
    
    async def notifier_candidats(session: AsyncSession, id_departement: int, texte: str,):
        try:
            result = await session.execute(
                select(Candidat.email)
                .where(Departement.id == id_departement)
            )

            emails_candidat = result.scalars().all()
            print(emails_candidat)
            
            for email in emails_candidat:
                await Admin.envoyer_email_candidat(email, texte)
            return True
        
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            )
    async def envoyer_email_candidat(email: str, texte: str,):
        smtp_server = os.getenv("SMTP_HOST")
        smtp_port = os.getenv("SMTP_PORT")  # SSL
        sender_email = os.getenv("SMTP_USER")
        sender_password = os.getenv("SMTP_PASSWORD")

        sujet = "Résultat de votre candidature"

        # Création de l'e-mail
        message = EmailMessage()
        message["Subject"] = sujet
        message["From"] = sender_email
        message["To"] = email
        message.set_content(texte)

        # Envoi via SMTP sécurisé
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
        except Exception as e:
            print(f"Erreur lors de l’envoi de l’e-mail : {e}")

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import logging

from fastapi import HTTPException
from datetime import date

import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

from app.models.admin import Admin as Admin_M
from app.models.offre import Offre
from app.models.detailPostuler import DetailPostuler
from app.models.poste import Poste
from app.models.cv import Cv
from app.models.candidat import Candidat

from app.dto.admin import AdminDTO
from app.dto.offre import OffreDTO
from app.dto.candidature import CandidatureDTO
from app.dto.candidature import CandidatureDTO
from app.dto.departement import DepartementDTO

class Admin:
    @staticmethod
    async def login(session: Session, login: str, mdp: str,) -> bool:
        """Retourne True si les identifiants sont corrects."""
        try:
            result = session.execute(
                select(Admin_M).where(Admin_M.nom == login, Admin_M.mdp == mdp)
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

    async def ajouter_offre(
        session: Session,
        titre: str,
        description: str,
        date_limite: date,
        id_poste: int,
        id_contrat: int,
    ) -> Admin_M:
        try:
            #ajouter le candidat
            offre = Offre(
                titre=titre,
                description=description,
                date_limite=date_limite,
                id_poste=id_poste,
                id_contrat=id_contrat
            )
            session.add(offre)
            session.commit()
            session.refresh(offre)

            return offre
        
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

    async def get_candidature(session: Session, id_poste: int,):
        """Retourne les candidatures"""
        try:
            stmt = (
                select(DetailPostuler)
                .options(
                    joinedload(DetailPostuler.candidat),
                    joinedload(DetailPostuler.poste),
                    joinedload(DetailPostuler.offre)
                )
                .where(DetailPostuler.id_poste == id_poste)
            )
            
            result =  session.execute(stmt)
            candidatures = result.unique().scalars().all()
            return candidatures

        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def get_dossier(session: Session, id_candidat: int, id_poste: int,):
        """Retourne le dossier d'un candidat"""
        try:
            stmt = (
                select(Cv)
                .where(Cv.id_candidat == id_candidat)
                .where(Cv.id_poste == id_poste)
            )
            
            result =  session.execute(stmt)
            dossier = result.unique().scalars().first()
            return dossier

        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
    
    async def notifier_candidats(session: Session, texte: str,):
        try:
            result = session.execute(
                select(Candidat.email)
            )

            emails_candidat = result.scalars().all()

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

    async def bloquer_debloquer_liste_candidats():
        try:
            chemin = os.path.join("bdd/liste.txt")
            with open(chemin, "r") as f:
                contenu = f.read()
            if contenu == "oui":
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("non")
            else:
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("oui")
            return True
        
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            )
        
    async def envoyer_email_candidat(email: str, texte: str,):
        load_dotenv()
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

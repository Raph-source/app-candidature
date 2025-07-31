from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


import joblib
import re
from PyPDF2 import PdfReader
import unicodedata
from pdf2image import convert_from_path
import pytesseract
import os

import logging
from fastapi import HTTPException

from app.models.candidat import Candidat as Candidat_M
from app.models.departement import Departement
from app.models.dossier import Dossier
from app.models.candidature import Candidature
from app.models.offre import Offre

from app.dto.candidat import CandidatDTO
from app.dto.departement import DepartementDTO
from app.dto.dossier import DossierDTO
from app.dto.candidature import CandidatureDTO
from app.dto.offre import OffreDTO


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
            return candidat
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
            departement = result.scalars().all()
            
            return departement
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def set_dossier(session: AsyncSession, id_candidat: int, id_departement: int, fichier: list,):
        """ajoute le dossier du candidat"""
        try:
            #vérifier l'existance du candidat
            result = await session.execute(
                select(Candidat_M).where(Candidat_M.id==id_candidat)
            )

            candidat = result.scalars().all()

            if len(candidat) < 1:
                return False
            
            dossier = Dossier(
                id_candidat=id_candidat,
                id_departement=id_departement,
                cv=fichier[0],
                lettre_motivation=fichier[1],
                diplome=fichier[2],
            )

            session.add(dossier)
            await session.commit()
            await session.refresh(dossier)

            return True
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
    
    async def get_offre(session: AsyncSession):
        """Retourne toutes les offres"""
        try:
            smtp = (
                    select(Offre)
                    .options(
                        joinedload(Offre.departement)
                    )
                )
            
            result = await session.execute(smtp)

            offres = result.scalars().all()
            return offres
    
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def postuler(session: AsyncSession, id_candidat: int, id_offre: int, id_departement: int, fichier: list):
        """ajoute une candidature"""
        try:
            #vérifier l'existance du candidat
            result = await session.execute(
                select(Candidat_M).where(Candidat_M.id==id_candidat)
            )

            candidat = result.scalars().all()

            if len(candidat) < 1:
                return "candidat not found"
            
            result = await session.execute(
                select(Departement.nom)
                .where(Departement.id==id_departement)
            )

            nom_departement = result.scalars().one_or_none()

            if(nom_departement == 'informatique'):
                response = await Candidat.candidature_info(session, id_candidat, id_offre, id_departement, fichier[0])
            else:
                return "département non trouvé"
            
            #ajouter le dossier dans la bdd
            dossier = Dossier(
                id_candidat=id_candidat,
                id_departement=id_departement,
                cv=fichier[0],
                lettre_motivation=fichier[1],
                diplome=fichier[2],
            )

            session.add(dossier)
            await session.commit()
            await session.refresh(dossier)
                              
            return response
    
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def nettoyer_texte(texte: str) -> str:
        # Supprimer les sauts de ligne et les espaces anormaux
        texte = texte.replace('\n', ' ').replace('\r', ' ')
        texte = re.sub(r'\s+', ' ', texte)  # Espaces multiples → un seul

        # Corriger les mots cassés (ex. : "expérienc e" → "expérience")
        texte = re.sub(r'exp[ée]rienc\s+e', 'expérience', texte, flags=re.IGNORECASE)
        
        # Normaliser les accents (é → é)
        texte = unicodedata.normalize("NFKC", texte)

        return texte.lower()

    async def extraire_texte_pdf(chemin_pdf: str) -> str:
        lecteur = PdfReader(chemin_pdf)
        texte = ""
        for page in lecteur.pages:
            texte += page.extract_text()
        return texte.lower()
    # Fonction pour extraire les features du CV
    async def extraire_features(texte: str) -> list[int]:
        texte = await Candidat.nettoyer_texte(texte=texte)

        feature_diplome = int(bool(re.search(r"(licence|master|bac\+3|bac\+5).*(informatique|computer)", texte)))
        feature_experience = int(bool(re.search(r"(\d+)\s*(ans|an)", texte)))
        feature_anglais = int("anglais" in texte or "english" in texte)
        feature_programmation = int(bool(re.search(r"\b(python|java|c\+\+|c#|javascript|php)\b", texte)))

        return [feature_diplome, feature_experience, feature_anglais, feature_programmation]

    async def candidature_info(session: AsyncSession, id_candidat: int, id_offre: int, id_departement: int, chemin_cv: str,):
        # Charger le modèle entraîné
        model = joblib.load("H:/app/storage/modele_informatique.pkl")

        chemin_cv = chemin_cv.replace('\\', '/')
        chemin_cv = "H:/app/" + chemin_cv

        #extraire le text du cv
        texte_cv = await Candidat.extraire_texte_pdf(chemin_cv)

        #extraire les features
        features = [await Candidat.extraire_features(texte_cv)]

        prediction = model.predict(features)

        if prediction[0] == 1:
            #ajouter la candidatue
            candidature = Candidature(id_candidat=id_candidat, id_offre=id_offre, id_departement=id_departement)
            session.add(candidature)
            await session.commit()
            await session.refresh(candidature)

            return True
        else:
            return False
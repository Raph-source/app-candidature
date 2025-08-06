from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


import joblib
import re
from PyPDF2 import PdfReader
import unicodedata
from pdf2image import convert_from_path
import pytesseract
import os
from datetime import date

import logging
from fastapi import HTTPException, UploadFile

from app.models.candidat import Candidat as Candidat_M
from app.models.poste import Poste
from app.models.cv import Cv
from app.models.detailPostuler import DetailPostuler
from app.models.offre import Offre
from app.models.compte import Compte

from app.dto.candidat import CandidatDTO
from app.dto.departement import DepartementDTO
from app.dto.dossier import DossierDTO
from app.dto.candidature import CandidatureDTO
from app.dto.offre import OffreDTO


class Candidat:
    #création du compte
    @staticmethod
    async def sign_in(
                        session: Session, 
                        nom: str, 
                        lieu: str, 
                        date_naiss: date, 
                        etat_civ: date,
                        age: int,
                        nationalite: str, 
                        email: str, 
                        login: str, 
                        mdp: str, 
                    ) -> Candidat_M:
        """retourne le Candidat si la création réeussie"""
        try:
            #Vérifier unicité e‑mail
            result = session.execute(
                select(Candidat_M).where(Candidat_M.email == email)
            )

            if result.scalar_one_or_none():
                return False
            
            #Vérifier unicité du login
            result = session.execute(
                select(Compte).where(Compte.login == login)
            )

            if result.scalar_one_or_none():
                return False
            
            #ajouter le candidat
            candidat = Candidat_M (
                nom=nom, 
                lieu=lieu, 
                date_naiss=date_naiss,
                etat_civ=etat_civ,
                age=age,
                nationalite=nationalite,
                email=email,
            )


            session.add(candidat)
            session.commit()
            session.refresh(candidat)

            #création du compte
            result = session.execute(
                select(Candidat_M).where(Candidat_M.email == email)
            )
            candidat = result.scalar_one_or_none()

            compte = Compte(login=login, password=mdp, id_candidat=candidat.id)

            session.add(compte)
            session.commit()
            session.refresh(compte)

            _= candidat.id
            
            return candidat
    
        except Exception as e:
            print(e)
            logging.exception("Erreur interne sign_in") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

    @staticmethod
    async def login(session: Session, login: str, mdp: str,):
        """Retourne le candidat si les identifiants sont corrects."""
        try:
            result = session.execute(
                select(Compte)
                .options(
                    joinedload(Compte.candidat)
                )
                .where(Compte.login == login, Compte.password == mdp)
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
    async def get_departement(session: Session):
        """retourne la liste des départements"""
        try:
            result = session.execute(
                select(Poste)
            )
            poste = result.scalars().all()
            
            return poste
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
  
    async def get_offre(session: Session):
        """Retourne toutes les offres"""
        try:
            smtp = (
                    select(Offre)
                    .options(
                        joinedload(Offre.poste)
                    )
                )
            
            result = session.execute(smtp)

            offres = result.scalars().all()
            return offres
    
        except Exception as e:
            print(e)
            logging.exception("Erreur interne") 
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e
        
    async def postuler(session: Session, id_candidat: int, id_offre: int, id_poste: int, cv: UploadFile):
        """ajoute une candidature"""
        try:
            #vérifier si le fichier est un pdf
            if not cv.filename.lower().endswith(".pdf"):
                return "fichier non pdf"

            #vérifier l'existance du candidat
            result = session.execute(
                select(Candidat_M).where(Candidat_M.id==id_candidat)
            )

            candidat = result.scalars().all()

            if len(candidat) < 1:
                return "candidat not found"
            
            result = session.execute(
                select(Poste.nom)
                .where(Poste.id==id_poste)
            )

            nom_poste = result.scalars().one_or_none()

            #création du dossier uploads
            UPLOAD_DIR = "uploads"
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            chemin = os.path.join(UPLOAD_DIR, f"{id_candidat}{id_poste}_{cv.filename}.pdf")
            with open(chemin, "wb") as f:
                f.write(await cv.read())

            if(nom_poste == 'informatique'):
                response = await Candidat.candidature_info(session, id_candidat, id_offre, id_poste, chemin)
            elif(nom_poste == 'comptabilité'):
                print("comptabilité")
            elif(nom_poste == 'logistique'):
                print("logistique")
            else:
                return "département non trouvé"
            
            #ajouter le dossier dans la bdd
            cv = Cv(
                id_candidat=id_candidat,
                id_poste=id_poste,
                chemin=chemin,
            )

            session.add(cv)
            session.commit()
            session.refresh(cv)
                              
            return response
    
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur",
            ) from e

    async def get_candidature(session: Session, id_poste: int,):
        """Retourne les candidatures"""
        try:
            chemin = os.path.join("bdd/liste.txt")
            with open(chemin, "r") as f:
                contenu = f.read()

            if contenu == "oui":
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
            else:
                return False


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

    async def candidature_info(session: Session, id_candidat: int, id_offre: int, id_poste: int, chemin_cv: str,):
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
            detailPostuler = DetailPostuler(id_candidat=id_candidat, id_offre=id_offre, id_poste=id_poste)
            session.add(detailPostuler)
            session.commit()
            session.refresh(detailPostuler) 

            return True
        else:
            return False
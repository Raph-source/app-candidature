from pydantic import BaseModel, EmailStr

from fastapi import UploadFile, Form, File
from pydantic import EmailStr
from typing import Optional
from pydantic import BaseModel
from typing import Annotated
from datetime import date


class ValidateurSignIn(BaseModel):
    """validateur pour la création d'uun compte candidat"""
    nom: str
    lieu: str
    date_naiss: date
    etat_civ: str
    age: int
    nationalite: str
    email: EmailStr
    login: str
    mdp: str

class ValidateurLogin(BaseModel):
    """validateur d'authentification candidat et admin"""
    login: str
    mdp: str

def ValidateurSignInForm(
    nom: str = Form(...),
    lieu: str = Form(...),
    date_naiss: date = Form(...),
    etat_civ: str = Form(...),
    age: int = Form(...),
    nationalite: str = Form(...),
    email: EmailStr = Form(...),
    login: str = Form(...),
    mdp: str = Form(...),
) -> ValidateurSignIn:
    return ValidateurSignIn(
        nom=nom,
        lieu=lieu,
        date_naiss=date_naiss,
        etat_civ=etat_civ,
        age=age,
        nationalite=nationalite,
        email=email,
        login=login,
        mdp=mdp
    )

def ValidateurLoginForm(
    login: str = Form(...),
    mdp: str = Form(...)
) -> ValidateurLogin:
    return ValidateurLogin(
        login=login,
        mdp=mdp
    )

class ValidateurPostuler(BaseModel):
    """validateur de postuler"""
    id_candidat: int
    id_offre: int
    id_poste: int
    cv: UploadFile

def ValidateurPostulerForm(
    id_candidat: Annotated[int, Form(...)],
    id_offre: Annotated[int, Form(...)],
    id_poste: Annotated[int, Form(...)],
    cv: Annotated[UploadFile, File(...)],
) -> ValidateurPostuler:
    return ValidateurPostuler(
        id_candidat=id_candidat,
        id_poste=id_poste,
        id_offre=id_offre,
        cv=cv
    )


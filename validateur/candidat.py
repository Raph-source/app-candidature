from pydantic import BaseModel, EmailStr

from fastapi import UploadFile, Form, File
from pydantic import EmailStr
from typing import Optional
from pydantic import BaseModel
from typing import Annotated


class ValidateurSignIn(BaseModel):
    """validateur pour la création d'uun compte candidat"""
    nom: str
    post_nom: Optional[str]
    prenom: str
    email: EmailStr
    mdp: str

class ValidateurLogin(BaseModel):
    """validateur d'authentification candidat et admin"""
    email: EmailStr
    mdp: str

def ValidateurSignInForm(
    nom: str = Form(...),
    post_nom: Optional[str] = Form(None),
    prenom: str = Form(...),
    email: EmailStr = Form(...),
    mdp: str = Form(...)
) -> ValidateurSignIn:
    return ValidateurSignIn(
        nom=nom,
        post_nom=post_nom,
        prenom=prenom,
        email=email,
        mdp=mdp
    )

def ValidateurLoginForm(
    email: EmailStr = Form(...),
    mdp: str = Form(...)
) -> ValidateurLogin:
    return ValidateurLogin(
        email=email,
        mdp=mdp
    )

class ValidateurPostuler(BaseModel):
    """validateur de postuler"""
    id_candidat: int
    id_offre: int
    id_departement: int

class FichiersUpload(BaseModel):
    """validateur de cv lettre de motivation et diplome"""
    cv: UploadFile
    lettre_motivation: UploadFile
    diplome: UploadFile

def ValidateurPostulerForm(
    id_candidat: Annotated[int, Form(...)],
    id_offre: Annotated[int, Form(...)],
    id_departement: Annotated[int, Form(...)],
    cv: Annotated[UploadFile, File(...)],
    lettre_motivation: Annotated[UploadFile, File(...)],
    diplome: Annotated[UploadFile, File(...)]
) -> tuple[ValidateurPostuler, list[UploadFile]]:
    return ValidateurPostuler(id_candidat=id_candidat, id_departement=id_departement, id_offre=id_offre), [cv, lettre_motivation, diplome]


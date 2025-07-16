from pydantic import BaseModel, EmailStr

from fastapi import Form
from pydantic import EmailStr
from typing import Optional
from pydantic import BaseModel

class ValidateurSignIn(BaseModel):
    nom: str
    post_nom: Optional[str]
    prenom: str
    email: EmailStr
    mdp: str

class ValidateurLogin(BaseModel):
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

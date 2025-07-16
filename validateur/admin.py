from pydantic import BaseModel, EmailStr
from datetime import date
from fastapi import Form
from pydantic import EmailStr
from typing import Optional
from pydantic import BaseModel

class ValidateurAjouterOffre(BaseModel):
    titre: str
    description: str
    date_limite: date
    idDepartement: int 

def ValidateurAjouterOffreForm(
    titre: str = Form(...),
    description: str = Form(...),
    date_limite: date = Form(...),
    idDepartement: int = Form(...)
) -> ValidateurAjouterOffre:
    return ValidateurAjouterOffre(
        titre=titre,
        description=description,
        date_limite=date_limite,
        idDepartement=idDepartement,
    )


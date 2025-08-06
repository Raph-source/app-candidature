from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from fastapi import Form, HTTPException

class ValidateurAjouterOffre(BaseModel):
    titre: str
    description: str
    date_limite: date
    id_poste: int
    id_contrat: int

    @field_validator("date_limite")
    @classmethod
    def valider_date_limite(cls, valeur):
        if valeur < date.today():
            raise HTTPException(status_code=401, detail="La date limite ne peut pas être inférieure à aujourd'hui.s")
        return valeur

def ValidateurAjouterOffreForm(
    titre: str = Form(...),
    description: str = Form(...),
    date_limite: date = Form(...),
    id_poste: int = Form(...),
    id_contrat: int = Form(...),
) -> ValidateurAjouterOffre:
    return ValidateurAjouterOffre(
        titre=titre,
        description=description,
        date_limite=date_limite,
        id_poste=id_poste,
        id_contrat=id_contrat,
    )

class ValidateurNotifierCandidat(BaseModel):
    texte: str

def ValidateurNotifierCandidatForm(
    texte: str = Form(...),
) -> ValidateurNotifierCandidat:
    return ValidateurNotifierCandidat(
        texte=texte,
    )
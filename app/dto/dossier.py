from pydantic import BaseModel
from datetime import date

class DossierDTO(BaseModel):
    id: int
    cv: str
    lettre_motivation: str
    diplome:       str
    date_depot:    date
    id_candidat:   int
    id_departement:int

    class Config:
        orm_mode = True
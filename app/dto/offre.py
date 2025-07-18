from pydantic import BaseModel
from datetime import date


class OffreDTO(BaseModel):
    id:          int
    titre:       str
    description: str
    date_limite: date
    id_departement: int

    class Config:
        orm_mode = True
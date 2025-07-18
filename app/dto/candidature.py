from pydantic import BaseModel
from datetime import date

class CandidatureDTO(BaseModel):
    id: int
    date_depot: date
    status: bool
    id_candidat: int
    id_offre: int

    class Config:
        orm_mode = True
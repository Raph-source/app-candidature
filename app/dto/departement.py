from pydantic import BaseModel

class DepartementDTO(BaseModel):
    id: int
    nom: str

    class Config:
        orm_mode = True
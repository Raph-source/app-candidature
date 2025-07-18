from pydantic import BaseModel, EmailStr

class AdminDTO(BaseModel):
    id: int
    nom: str
    email: EmailStr
    mdp: str

    class Config:
        orm_mode = True
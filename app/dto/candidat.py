from pydantic import BaseModel, EmailStr

class CandidatDTO(BaseModel):
    id: int
    date_depot: str
    post_nom: str
    prenom: str
    email: EmailStr
    mdp: str

    class Config:
        orm_mode = True
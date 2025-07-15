from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from validateur.candidat import ValidateurSignIn, ValidateurSignInForm, validateurLogin
from database import AsyncSessionLocal
from typing import AsyncGenerator

from app.controllers.candidat import Candidat as CandidatController

router = APIRouter(prefix="/candidats", tags=["Candidats"])

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]    

@router.post("/signup", status_code=201)
async def sign_up( db: DBSession, payload: ValidateurSignIn = Depends(ValidateurSignInForm),):
    reponse =  await CandidatController.sign_in(db, **payload.model_dump())
    if not reponse:
        raise HTTPException(status_code=409, detail="le compte exist")
    return reponse

@router.post("/login")
async def login(payload: validateurLogin, db: DBSession):
    ok = await CandidatController.login(db, **payload.model_dump())
    if not ok:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"message": "Connexion réussie"}

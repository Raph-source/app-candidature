from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from validateur.candidat import *
from validateur.admin import *
from database import AsyncSessionLocal
from typing import AsyncGenerator

from app.controllers.admin import Admin as AdminController
from contextlib import asynccontextmanager

router = APIRouter(prefix="/admin", tags=["admin"])

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]    

#==================== LES REQUETES POST ===================================
@router.post("/login", status_code=201)
async def login(
    db: DBSession, 
    payload: ValidateurLogin = Depends(ValidateurLoginForm),
):
    ok = await AdminController.login(db, **payload.model_dump())
    if not ok:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"message": "Connexion réussie"}

@router.post("/ajouter-offre", status_code=201)
async def ajouter_offre(
    db: DBSession,
    payload: ValidateurAjouterOffre = Depends(ValidateurAjouterOffreForm),
):
    reponse =  await AdminController.ajouter_offre(db, **payload.model_dump())
    return reponse

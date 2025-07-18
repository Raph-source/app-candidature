from fastapi import APIRouter, Depends, HTTPException, Path
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

#==================== LES REQUETES GET ===================================
@router.get("/candidatures/{id_departement}", status_code=200)
async def get_candidature(db: DBSession, id_departement: int = Path(..., gt=0)):
    candidature = await AdminController.get_candidature(db, id_departement)
    return candidature

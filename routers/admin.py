from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from validateur.candidat import *
from validateur.admin import *
from database import SessionLocal
from typing import AsyncGenerator

from app.controllers.admin import Admin as AdminController
from contextlib import asynccontextmanager

router = APIRouter(prefix="/admin", tags=["admin"])

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#==================== LES REQUETES POST ===================================
@router.post("/login", status_code=201)
async def login(
    db: Session = Depends(get_db), 
    payload: ValidateurLogin = Depends(ValidateurLoginForm),
):
    ok = await AdminController.login(db, **payload.model_dump())
    if not ok:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"message": "Connexion réussie"}

@router.post("/ajouter-offre", status_code=201)
async def ajouter_offre(
    db: Session = Depends(get_db),
    payload: ValidateurAjouterOffre = Depends(ValidateurAjouterOffreForm),
):
    reponse =  await AdminController.ajouter_offre(db, **payload.model_dump())
    return reponse

@router.post("/notifier-candidat", status_code=200)
async def ajouter_offre(
    db: Session = Depends(get_db),
    payload: ValidateurNotifierCandidat = Depends(ValidateurNotifierCandidatForm),
):
    reponse =  await AdminController.notifier_candidats(db, **payload.model_dump())
    return reponse

#==================== LES REQUETES GET ===================================
@router.get("/candidatures/{id_poste}", status_code=200)
async def get_candidature(db: Session = Depends(get_db), id_poste: int = Path(..., gt=0)):
    candidature = await AdminController.get_candidature(db, id_poste)
    return candidature

@router.get("/cv/{id_candidat}/{id_poste}", status_code=200)
async def get_dossier(
    db: Session = Depends(get_db),
    id_candidat: int = Path(..., gt=0),
    id_poste: int = Path(..., gt=0)
):
    candidature = await AdminController.get_dossier(db, id_candidat, id_poste)
    return candidature

@router.get("/bloquer-debloquer-liste", status_code=200)
async def departement():
    departement = await AdminController.bloquer_debloquer_liste_candidats()
    return departement

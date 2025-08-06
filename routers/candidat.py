from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
import os

from validateur.candidat import *
from database import SessionLocal
from typing import AsyncGenerator

from app.controllers.candidat import Candidat as CandidatController

router = APIRouter(prefix="/candidat", tags=["Candidat"])

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[AsyncSession, Depends(get_db)]    

#==================== LES REQUETES POST ===================================

@router.post("/signup", status_code=201)
async def sign_up(
    db: Session = Depends(get_db),
    payload: ValidateurSignIn = Depends(ValidateurSignInForm),
):
    reponse =  await CandidatController.sign_in(db, **payload.model_dump())
    
    if not reponse:
        raise HTTPException(status_code=409, detail="le compte exist")
    return reponse

@router.post("/login", status_code=200)
async def login(
    db: Session = Depends(get_db),
    payload: ValidateurLogin = Depends(ValidateurLoginForm),
):
    candidat = await CandidatController.login(db, **payload.model_dump())
    if not candidat:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return candidat

@router.post("/postuler", status_code=201)
async def set_candidature(
    db: Session = Depends(get_db),
    payload: ValidateurPostuler = Depends(ValidateurPostulerForm),
):

    reponse = await CandidatController.postuler(db, **payload.model_dump())

    if reponse == True:
        return {"message" : "SUCCESS"}
    elif reponse == False:
        raise HTTPException(status_code=400, detail=f"cv non conforme")
    elif reponse == "candidat not found":
        raise HTTPException(status_code=400, detail=f"le candidat n'existe pas")
    elif reponse == "fichier non pdf":
        raise HTTPException(status_code=400, detail=f"fichier non pdf")
    elif reponse == "département non trouvé":
        raise HTTPException(status_code=400, detail=f"département non trouvé")

#==================== LES REQUETES GET ===================================
@router.get("/departement", status_code=200)
async def departement(db: Session = Depends(get_db),):
    departement = await CandidatController.get_departement(db)
    return departement

@router.get("/offres", status_code=200)
async def get_offre(db: Session = Depends(get_db),):
    departement = await CandidatController.get_offre(db)
    return departement

@router.get("/candidat-retenu/{id_poste}", status_code=200)
async def get_candidat_retenu(db: Session = Depends(get_db), id_poste: int = Path(..., gt=0)):
    candidature = await CandidatController.get_candidature(db, id_poste)
    return candidature


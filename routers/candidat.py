from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

from validateur.candidat import *
from database import AsyncSessionLocal
from typing import AsyncGenerator

from app.controllers.candidat import Candidat as CandidatController

router = APIRouter(prefix="/candidat", tags=["Candidat"])

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]    

#==================== LES REQUETES POST ===================================
@router.post("/signup", status_code=201)
async def sign_up(
    db: DBSession,
    payload: ValidateurSignIn = Depends(ValidateurSignInForm),
):
    reponse =  await CandidatController.sign_in(db, **payload.model_dump())
    if not reponse:
        raise HTTPException(status_code=409, detail="le compte exist")
    return reponse

@router.post("/login", status_code=200)
async def login(
    db: DBSession,
    payload: ValidateurLogin = Depends(ValidateurLoginForm),
):
    ok = await CandidatController.login(db, **payload.model_dump())
    if not ok:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"message": "Connexion réussie"}

#création du dossier uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ajouter-dossier", status_code=201)
async def ajouter_dossier(
    db: DBSession,
    data: tuple[ValidateurUpload, List[UploadFile]] = Depends(ValidateurUploadForm),
):
    payload, fichiers = data
    chemins = []

    for idx, fichier in enumerate(fichiers, start=1):
        if not fichier.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Le fichier {idx} n'est pas un PDF valide.")

        chemin = os.path.join(UPLOAD_DIR, f"{payload.id_candidat}{payload.id_departement}_fichier{idx}.pdf")
        with open(chemin, "wb") as f:
            f.write(await fichier.read())

        chemins.append(chemin)
    
    reponse = await CandidatController.set_dossier(db, payload.id_candidat, payload.id_departement, chemins,)

    if not reponse:
        raise HTTPException(status_code=400, detail=f"le candidat n'existe pas")
    return {"message" : "dossier ajouté avec succès"}

@router.post("/postuler", status_code=201)
async def sign_up(
    db: DBSession,
    payload: ValidateurPostuler = Depends(ValidateurPostulerForm),
):
    reponse =  await CandidatController.postuler(db, **payload.model_dump())
    return reponse

#==================== LES REQUETES GET ===================================
@router.get("/departement", status_code=200)
async def departement(db: DBSession,):
    departement = await CandidatController.get_departement(db)
    return departement

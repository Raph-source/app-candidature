from fastapi import FastAPI
from routers.candidat import router as candidat_router
from routers.admin import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",  # Vite.js (React) en développement
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autorise les requêtes venant de ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

app.include_router(candidat_router, prefix="")
app.include_router(admin_router, prefix="")

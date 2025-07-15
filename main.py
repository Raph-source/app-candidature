from fastapi import FastAPI
from routers.candidat import router as candidat_router

app = FastAPI()
app.include_router(candidat_router, prefix="")

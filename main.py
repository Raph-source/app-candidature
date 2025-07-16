from fastapi import FastAPI
from routers.candidat import router as candidat_router
from routers.admin import router as admin_router

app = FastAPI()
app.include_router(candidat_router, prefix="")
app.include_router(admin_router, prefix="")

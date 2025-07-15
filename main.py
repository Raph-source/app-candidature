# app/main.py
from fastapi import FastAPI
from database import engine
from models import Base   # déclenche l'import de toutes les tables

app = FastAPI()



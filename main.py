from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine, get_db
import tracemalloc
import logging
from app.routers import formulario
from app.routers import auth


tracemalloc.start()

logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9000",
    "http://127.0.0.1",
    "http://127.0.0.1:9000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_tables():
    print('Creando tablas...')
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas con éxito")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")



create_tables()

# app.include_router(admin.router)
app.include_router(formulario.router)
app.include_router(auth.router)
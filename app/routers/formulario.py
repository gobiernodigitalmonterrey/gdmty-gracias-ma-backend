from fastapi import APIRouter,Depends, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.schemas import FormularioMultipart
from app.views import formularioView


router = APIRouter(
    prefix="/formulario",
    tags=["Formulario"]
)

@router.post("/enviar_formulario", status_code=status.HTTP_201_CREATED)
async def create_admin(formulario: FormularioMultipart = Depends(), db: Session = Depends(get_db)):
    support = await formularioView.create_formulario(formulario, db)
    return support
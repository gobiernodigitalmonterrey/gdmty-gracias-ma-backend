from fastapi import APIRouter,Depends, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas import FormularioMultipart
from app.views import formularioView
import logging

router = APIRouter(
    prefix="/formulario",
    tags=["Formulario"]
)

@router.post("/enviar_formulario")
async def enviar_formulario(
    formulario: FormularioMultipart = Depends(),
    db: Session = Depends(get_db)
):
    logging.info(f"Iniciando procesamiento de formulario para: {formulario.nombre}")
    support = await formularioView.create_formulario(formulario, db)
    logging.info(f"Formulario procesado exitosamente: {support}")
    return support
from fastapi import APIRouter,Depends, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas import FormularioMultipart
from app.views import formularioView


router = APIRouter(
    prefix="/formulario",
    tags=["Formulario"]
)

@router.post("/enviar_formulario")
async def enviar_formulario(
    formulario: FormularioMultipart = Depends(),
    db: Session = Depends(get_db)
):
    support = await formularioView.create_formulario(formulario, db)
    return support
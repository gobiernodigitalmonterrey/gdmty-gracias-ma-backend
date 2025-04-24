from sqlalchemy.orm import Session
from app.db.models import Formulario as FormularioModel
from app.schemas import FormularioMultipart as FormularioSchema
from fastapi import HTTPException
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def validar_formulario(formulario: FormularioSchema):
    if len(formulario.curp) != 18:
        raise HTTPException(status_code=400, detail="La CURP debe tener 18 caracteres")
    if len(formulario.telefono) != 10:
        raise HTTPException(status_code=400, detail="El teléfono debe tener 10 dígitos")
    if not (10000 <= formulario.codigo_postal <= 99999):
        raise HTTPException(status_code=400, detail="El código postal debe tener 5 dígitos")


async def guardar_archivo(file, filename):
    if not file:
        return None
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return path


async def create_formulario(formulario: FormularioSchema, db: Session):
    validar_formulario(formulario)

    ine_frontal_path = await guardar_archivo(formulario.ine_frontal, f"{formulario.curp}_ine_frontal.{formulario.ine_frontal.filename.split('.')[-1]}") if formulario.ine_frontal else None
    ine_reverso_path = await guardar_archivo(formulario.ine_reverso, f"{formulario.curp}_ine_reverso.{formulario.ine_reverso.filename.split('.')[-1]}") if formulario.ine_reverso else None
    acta_nacimiento_path = await guardar_archivo(formulario.acta_nacimiento, f"{formulario.curp}_acta.{formulario.acta_nacimiento.filename.split('.')[-1]}") if formulario.acta_nacimiento else None

    campos_formulario = formulario.dict(exclude_unset=True)
    campos_formulario.update({
        "ine_frontal": ine_frontal_path,
        "ine_reverso": ine_reverso_path,
        "acta_nacimiento": acta_nacimiento_path
    })

    nuevo_formulario = FormularioModel(**campos_formulario)

    try:
        db.add(nuevo_formulario)
        db.commit()
        db.refresh(nuevo_formulario)
        return {"mensaje": "Formulario registrado con éxito", "id": nuevo_formulario.id}
    except Exception as e:
        for path in [ine_frontal_path, ine_reverso_path, acta_nacimiento_path]:
            if path and os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=400, detail=f"Error al registrar formulario: {str(e)}")

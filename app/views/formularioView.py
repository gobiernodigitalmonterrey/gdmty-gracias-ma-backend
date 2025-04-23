from sqlalchemy.orm import Session
from app.db.models import Formulario as FormularioModel
from app.schemas import FormularioMultipart as FormularioSchema
from fastapi import HTTPException
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_formulario(formulario: FormularioSchema ,db: Session):
    # Validar CURP (18 caracteres)
    if len(formulario.curp) != 18:
        raise HTTPException(status_code=400, detail="La CURP debe tener 18 caracteres")

    # Validar teléfono (10 dígitos)
    if len(formulario.telefono) != 10:
        raise HTTPException(status_code=400, detail="El teléfono debe tener 10 dígitos")

    # Validar código postal (5 dígitos)
    if formulario.codigo_postal < 10000 or formulario.codigo_postal > 99999:
        raise HTTPException(status_code=400, detail="El código postal debe tener 5 dígitos")

    # Guardar archivos si fueron proporcionados
    ine_frontal_path = None
    ine_reverso_path = None
    acta_nacimiento_path = None

    if formulario.ine_frontal:
        ine_frontal_path = f"{UPLOAD_DIR}/{formulario.curp}_ine_frontal.{formulario.ine_frontal.filename.split('.')[-1]}"
        with open(ine_frontal_path, "wb") as f:
            f.write(await formulario.ine_frontal.read())

    if formulario.ine_reverso:
        ine_reverso_path = f"{UPLOAD_DIR}/{formulario.curp}_ine_reverso.{formulario.ine_reverso.filename.split('.')[-1]}"
        with open(ine_reverso_path, "wb") as f:
            f.write(await formulario.ine_reverso.read())

    if formulario.acta_nacimiento:
        acta_nacimiento_path = f"{UPLOAD_DIR}/{formulario.curp}_acta.{formulario.acta_nacimiento.filename.split('.')[-1]}"
        with open(acta_nacimiento_path, "wb") as f:
            f.write(await formulario.acta_nacimiento.read())

    # Crear nuevo registro en la base de datos
    nuevo_formulario = FormularioModel(
        nombre=formulario.nombre,
        apellido_paterno=formulario.apellido_paterno,
        apellido_materno=formulario.apellido_materno,
        curp=formulario.curp,
        correo_electronico=formulario.correo_electronico,
        telefono=formulario.telefono,
        calle=formulario.calle,
        numero=formulario.numero,
        colonia=formulario.colonia,
        codigo_postal=formulario.codigo_postal,
        ine_frontal=ine_frontal_path,
        ine_reverso=ine_reverso_path,
        acta_nacimiento=acta_nacimiento_path
    )

    try:
        db.add(nuevo_formulario)
        db.commit()
        db.refresh(nuevo_formulario)
        return {"mensaje": "Formulario registrado con éxito", "id": nuevo_formulario.id}
    except Exception as e:
        # Si hay error, eliminar los archivos guardados
        for path in [ine_frontal_path, ine_reverso_path, acta_nacimiento_path]:
            if path and os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=400, detail=f"Error al registrar formulario: {str(e)}")
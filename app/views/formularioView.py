import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from google.cloud import storage
from google.oauth2 import service_account
from app.db.models import Formulario as FormularioModel
from app.schemas import FormularioMultipart as FormularioSchema
import logging

GOOGLE_CREDENTIALS_PATH = os.getenv('PATH_KEYS_JSON', '')
BUCKET_NAME = os.getenv('BUCKET_NAME', '')
credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH)
storage_client = storage.Client(credentials=credentials)
bucket = storage_client.get_bucket(BUCKET_NAME)

def validar_formulario(form: FormularioSchema):
    if len(form.curp) != 18:
        raise HTTPException(status_code=400, detail="La CURP debe tener 18 caracteres")
    if len(form.telefono) != 10:
        raise HTTPException(status_code=400, detail="El teléfono debe tener 10 dígitos")
    if not (10000 <= form.codigo_postal <= 99999):
        raise HTTPException(status_code=400, detail="El código postal debe tener 5 dígitos")

async def subir_archivo(file, filename):
    if not file:
        return None
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

async def create_formulario(formulario: FormularioSchema, db: Session):
    validar_formulario(formulario)

    logging.info("Validando formulario...")

    campos = formulario.dict(exclude_unset=True)
    campos.update({"ine_frontal": None, "ine_reverso": None, "acta_nacimiento": None})
    nuevo_formulario = FormularioModel(**campos)

    archivos_subidos = []

    try:
        db.add(nuevo_formulario)
        db.commit()
        db.refresh(nuevo_formulario)

        uploads = {
            "ine_frontal": formulario.ine_frontal,
            "ine_reverso": formulario.ine_reverso,
            "acta_nacimiento": formulario.acta_nacimiento,
        }

        carpeta_curp = f"{formulario.nombre} {formulario.apellido_paterno} {formulario.apellido_materno} - {formulario.curp}/"

        for campo, archivo in uploads.items():
            logging.info("entrando al for")
            if archivo:
                ext = archivo.filename.split('.')[-1]
                filename = f"{carpeta_curp}{campo}.{ext}"
                try:
                    url = await subir_archivo(archivo, filename)
                    setattr(nuevo_formulario, campo, url)
                    archivos_subidos.append(filename)
                except Exception as e:
                    for archivo in archivos_subidos:
                        blob = bucket.blob(archivo)
                        blob.delete()
                    raise HTTPException(status_code=400, detail=f"Error al subir el archivo {campo}: {str(e)}")

        db.commit()
        db.refresh(nuevo_formulario)

        return {"mensaje": "Formulario registrado con éxito", "id": nuevo_formulario.id}

    except Exception as e:
        db.rollback()

        for archivo in archivos_subidos:
            blob = bucket.blob(archivo)
            blob.delete()

        raise HTTPException(status_code=400, detail=f"Error al registrar formulario: {str(e)}")

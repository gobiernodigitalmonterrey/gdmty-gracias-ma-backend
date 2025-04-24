from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional
from app.decorators.DecoratorsFormulario import as_form

@as_form
class FormularioMultipart(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    correo_electronico: str
    telefono: str
    calle: str
    numero: int
    colonia: str
    codigo_postal: int
    ine_frontal: Optional[UploadFile] = None
    ine_reverso: Optional[UploadFile] = None
    acta_nacimiento: Optional[UploadFile] = None

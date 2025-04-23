from fastapi import UploadFile, File, Form
from typing import Optional

class FormularioMultipart:
    def __init__(
        self,
        nombre: str = Form(...),
        apellido_paterno: str = Form(...),
        apellido_materno: str = Form(...),
        curp: str = Form(...),
        correo_electronico: str = Form(...),
        telefono: str = Form(...),
        calle: str = Form(...),
        numero: int = Form(...),
        colonia: str = Form(...),
        codigo_postal: int = Form(...),
        ine_frontal: Optional[UploadFile] = File(None),
        ine_reverso: Optional[UploadFile] = File(None),
        acta_nacimiento: Optional[UploadFile] = File(None),
    ):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.curp = curp
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.calle = calle
        self.numero = numero
        self.colonia = colonia
        self.codigo_postal = codigo_postal
        self.ine_frontal = ine_frontal
        self.ine_reverso = ine_reverso
        self.acta_nacimiento = acta_nacimiento

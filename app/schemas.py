from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from app.decorators.DecoratorsFormulario import as_form
from typing import Optional, Union
from datetime import datetime

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



class User(BaseModel):
    name:str
    surname:str
    username:str
    password:str
    number_phone:str
    mail:str
    rango:str = 'user'
    creation:datetime = datetime.now()

class LoginEmail(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
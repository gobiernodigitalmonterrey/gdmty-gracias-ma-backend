from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class Formulario(Base):
    __tablename__ = "formulario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String,nullable=False)
    apellido_paterno = Column(String,nullable=False)
    apellido_materno = Column(String,nullable=False)
    curp = Column(String(18), nullable=False, unique=True)
    correo_electronico = Column(String, nullable=False, unique=True)
    telefono = Column(String(10), nullable=False, unique=True)
    calle = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    colonia = Column(String, nullable=False)
    codigo_postal = Column(Integer, nullable=False)
    ine_frontal = Column(String, nullable=True)
    ine_reverso = Column(String, nullable=True)
    acta_nacimiento = Column(String, nullable=True)
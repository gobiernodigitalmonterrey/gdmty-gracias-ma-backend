from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class Formulario(Base):
    __tablename__ = "formulario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100),nullable=False)
    apellido_paterno = Column(String(100),nullable=False)
    apellido_materno = Column(String(100),nullable=False)
    curp = Column(String(18), nullable=False, unique=True)
    correo_electronico = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(10), nullable=False, unique=True)
    calle = Column(String(150), nullable=False)
    numero = Column(Integer, nullable=False)
    colonia = Column(String(150), nullable=False)
    codigo_postal = Column(Integer, nullable=False)
    ine_frontal = Column(String(255), nullable=True)
    ine_reverso = Column(String(255), nullable=True)
    acta_nacimiento = Column(String(255), nullable=True)
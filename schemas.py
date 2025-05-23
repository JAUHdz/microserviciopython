### schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class DireccionBase(BaseModel):
    calle: Optional[str]
    numero: Optional[str]
    colonia: Optional[str]
    municipio: Optional[str]
    estado: Optional[str]
    cp: Optional[str]

class IneBase(BaseModel):
    clave_elector: str

class PersonaBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    curp: str

class PersonaCreate(PersonaBase):
    direccion: DireccionBase
    ine: IneBase

class Direccion(DireccionBase):
    class Config:
        orm_mode = True

class Ine(IneBase):
    class Config:
        orm_mode = True

class Persona(PersonaBase):
    direccion: Optional[Direccion] = None
    ine: Optional[Ine] = None

    class Config:
        orm_mode = True

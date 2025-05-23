### models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from database import Base

class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    fecha_nacimiento = Column(Date)
    sexo = Column(CHAR(1))
    curp = Column(String(18), unique=True, nullable=False)

    direccion = relationship("Direccion", back_populates="persona", uselist=False)
    ine = relationship("Ine", back_populates="persona", uselist=False)

class Direccion(Base):
    __tablename__ = "direccion"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("persona.id"))
    calle = Column(String(150))
    numero = Column(String(100))
    colonia = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(100))
    cp = Column(String(10))

    persona = relationship("Persona", back_populates="direccion")

class Ine(Base):
    __tablename__ = "ine"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("persona.id"))
    clave_elector = Column(String(20), unique=True)

    persona = relationship("Persona", back_populates="ine")


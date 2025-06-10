import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProfesionUsuario(Base):
    __tablename__ = 'profesionesusuario'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    persona_id = Column(Integer, nullable=False)
    profesion_id = Column(CHAR(36), nullable=False) 

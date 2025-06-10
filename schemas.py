from pydantic import BaseModel
from uuid import UUID

# ----------------
# ProfesionUsuario base
# ----------------
class ProfesionUsuarioBase(BaseModel):
    persona_id: int
    profesion_id: UUID  # <-- cambia a UUID

class ProfesionUsuarioCreate(ProfesionUsuarioBase):
    pass

class ProfesionUsuario(ProfesionUsuarioBase):
    id: UUID

    class Config:
        orm_mode = True

# ----------------
# Detalle con nombre de persona y profesión
# ----------------
class ProfesionUsuarioDetalle(BaseModel):
    id: UUID
    persona_id: int
    nombre_persona: str
    profesion_id: UUID  # <-- cambia a UUID
    nombre_profesion: str

    class Config:
        orm_mode = True

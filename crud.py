from sqlalchemy.orm import Session
import models, schemas
import requests
from fastapi import HTTPException
from datetime import date
import uuid
from uuid import UUID
from typing import List

# ProfesionesUsuario
def persona_existe(persona_id) -> bool:
    try:
        persona_id = str(persona_id).strip().lower()
        response = requests.get("https://microservicioinenew.onrender.com/api/ine/consulta")
        if response.status_code == 200:
            personas = response.json()
            return any(
                str(p['persona_id']).strip().lower() == persona_id
                for p in personas
            )
    except Exception as e:
        print("Error en persona_existe:", e)
        return False
    return False



def profesion_existe(profesion_id: UUID) -> bool:
    try:
        response = requests.get("https://python-eic3.onrender.com/profesiones/")
        if response.status_code == 200:
            profesiones = response.json()
            return any(p['id'] == str(profesion_id) for p in profesiones)
    except Exception:
        return False
    return False

def crear_profesion_usuario(db: Session, relacion: schemas.ProfesionUsuarioCreate):
    if not persona_existe(relacion.persona_id):
        raise HTTPException(status_code=404, detail="persona_id no existe en el microservicio INE")

    if not profesion_existe(relacion.profesion_id):
        raise HTTPException(status_code=404, detail="profesion_id no existe en el microservicio de Profesiones")

    nueva_relacion = models.ProfesionUsuario(
        id=str(uuid.uuid4()),
        persona_id=str(relacion.persona_id),
        profesion_id=str(relacion.profesion_id)  # <-- aquí conviertes UUID a string
    )
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion


def obtener_profesiones_usuario(db: Session):
    return db.query(models.ProfesionUsuario).all()

def obtener_profesiones_usuario_por_profesion(db: Session, profesion_id: UUID):
    return db.query(models.ProfesionUsuario).filter(models.ProfesionUsuario.profesion_id == str(profesion_id)).all()

def obtener_detalle_profesiones_usuario(db: Session):
    relaciones = db.query(models.ProfesionUsuario).all()

    # Obtener profesiones desde el microservicio externo
    try:
        profesiones_response = requests.get("https://python-eic3.onrender.com/profesiones/")
        profesiones = profesiones_response.json() if profesiones_response.status_code == 200 else []
        profesiones_dict = {p['id']: p['nombre'] for p in profesiones}
    except:
        profesiones_dict = {}

    # Obtener personas desde el microservicio INE
    try:
        personas_response = requests.get("https://microservicioinenew.onrender.com/api/ine/consulta")
        personas = personas_response.json() if personas_response.status_code == 200 else []
        personas_dict = {p['persona_id']: p['nombre'] for p in personas}
    except:
        personas_dict = {}

    resultado = []
    for r in relaciones:
        resultado.append({
            "id": r.id,
            "persona_id": r.persona_id,
            "nombre_persona": personas_dict.get(r.persona_id, "Desconocido"),
            "profesion_id": r.profesion_id,
            "nombre_profesion": profesiones_dict.get(r.profesion_id, "Desconocido")
        })
    return resultado


def obtener_profesiones_usuario_por_nombre_profesion(db: Session, nombre_profesion: str) -> List[schemas.ProfesionUsuarioDetalle]:
    # 1. Consultar microservicio para obtener profesión por nombre
    url = f"https://python-eic3.onrender.com/profesiones/nombre/{nombre_profesion}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Profesión no encontrada en microservicio externo")
        profesion_data = response.json()
        profesion_id = profesion_data.get('id')
        if not profesion_id:
            raise HTTPException(status_code=404, detail="ID de profesión no encontrado en respuesta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar microservicio de profesiones: {str(e)}")

    # 2. Obtener relaciones con ese profesion_id
    relaciones = db.query(models.ProfesionUsuario).filter(models.ProfesionUsuario.profesion_id == profesion_id).all()

    # 3. Obtener datos de personas para el detalle
    try:
        personas_response = requests.get("https://microservicioinenew.onrender.com/api/ine/consulta")
        personas = personas_response.json() if personas_response.status_code == 200 else []
        personas_dict = {p['persona_id']: p['nombre'] for p in personas}
    except:
        personas_dict = {}

    # 4. Construir resultado con detalle
    resultado = []
    for r in relaciones:
        resultado.append({
            "id": r.id,
            "persona_id": r.persona_id,
            "nombre_persona": personas_dict.get(r.persona_id, "Desconocido"),
            "profesion_id": r.profesion_id,
            "nombre_profesion": profesion_data.get('nombre', "Desconocido")
        })
    return resultado



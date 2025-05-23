from sqlalchemy.orm import Session
import models, schemas

def crear_persona(db: Session, persona_data: schemas.PersonaCreate):
    persona = models.Persona(
        nombre=persona_data.nombre,
        apellido_paterno=persona_data.apellido_paterno,
        apellido_materno=persona_data.apellido_materno,
        fecha_nacimiento=persona_data.fecha_nacimiento,
        sexo=persona_data.sexo,
        curp=persona_data.curp
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)

    direccion = models.Direccion(persona_id=persona.id, **persona_data.direccion.dict())
    ine = models.Ine(persona_id=persona.id, **persona_data.ine.dict())

    db.add(direccion)
    db.add(ine)
    db.commit()

    return persona

def obtener_persona_por_curp(db: Session, curp: str):
    return db.query(models.Persona).filter(models.Persona.curp == curp).first()

def obtener_persona_por_id(db: Session, persona_id: int):
    return db.query(models.Persona).filter(models.Persona.id == persona_id).first()

def obtener_personas(db: Session):
    return db.query(models.Persona).all()

def eliminar_persona_por_curp(db: Session, curp: str):
    persona = db.query(models.Persona).filter(models.Persona.curp == curp).first()
    if persona:
        # Eliminar dirección
        direccion = db.query(models.Direccion).filter(models.Direccion.persona_id == persona.id).first()
        if direccion:
            db.delete(direccion)

        # Eliminar ine
        ine = db.query(models.Ine).filter(models.Ine.persona_id == persona.id).first()
        if ine:
            db.delete(ine)

        # Finalmente eliminar la persona
        db.delete(persona)
        db.commit()
    return persona


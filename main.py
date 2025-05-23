from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from typing import List
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI desde Windows!"}

@app.post("/personas/", response_model=schemas.Persona)
def crear_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    return crud.crear_persona(db, persona)

@app.get("/personas/curp/{curp}", response_model=schemas.Persona)
def obtener_por_curp(curp: str, db: Session = Depends(get_db)):
    persona = crud.obtener_persona_por_curp(db, curp)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.get("/obtener/personas", response_model=List[schemas.Persona])
def obtener_personas(db: Session = Depends(get_db)):
    persona = crud.obtener_personas(db)
    if not persona:
        raise HTTPException(status_code=404, detail="Personas no encontrada")
    return persona

@app.get("/personas/{persona_id}", response_model=schemas.Persona)
def obtener_por_id(persona_id: int, db: Session = Depends(get_db)):
    persona = crud.obtener_persona_por_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.delete("/personas/curp/{curp}")
def eliminar_por_curp(curp: str, db: Session = Depends(get_db)):
    persona = crud.eliminar_persona_por_curp(db, curp)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"mensaje": "Persona eliminada correctamente"}

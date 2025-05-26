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

# RUTAS PROFESIONES-USUARIO
@app.post("/profesionesusuario/", response_model=schemas.ProfesionUsuario)
def crear_profesion_usuario(data: schemas.ProfesionUsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_profesion_usuario(db, data)

@app.get("/profesionesusuario/", response_model=List[schemas.ProfesionUsuario])
def obtener_profesiones_usuario(db: Session = Depends(get_db)):
    return crud.obtener_profesiones_usuario(db)

@app.get("/profesionesusuario/profesion/{profesion_id}", response_model=List[schemas.ProfesionUsuario])
def obtener_profesiones_usuario_por_profesion(profesion_id: int, db: Session = Depends(get_db)):
    return crud.obtener_profesiones_usuario_por_profesion(db, profesion_id)

@app.get("/profesionesusuario/detalle/", response_model=List[schemas.ProfesionUsuarioDetalle])
def obtener_detalle_profesiones_usuario(db: Session = Depends(get_db)):
    return crud.obtener_detalle_profesiones_usuario(db)

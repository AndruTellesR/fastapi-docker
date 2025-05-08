from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import json
import os

# Importamos nuestros modelos de la base de datos y esquemas Pydantic
from .database import get_db, Note as NoteModel
from .schemas import Note, NoteCreate

app = FastAPI()


@app.get("/")
async def root():
    """Página principal que da la bienvenida a nuestra API de notas"""
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }


@app.get("/notes", response_model=list[Note])
async def get_notes(db: Session = Depends(get_db)):
    """Obtiene todas las notas guardadas en la base de datos
    
    Para probar: Haz una petición GET a http://localhost:8000/notes
    Si estás usando curl: curl http://localhost:8000/notes
    """
    try:
        # Consultamos todas las notas de la base de datos
        notes = db.query(NoteModel).all()
        return notes
    except SQLAlchemyError as e:
        # Si hay un error con la base de datos, devolvemos un mensaje claro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(request: Request, db: Session = Depends(get_db)):
    """Crea una nueva nota en la base de datos
    
    Para probar: Envía una petición POST a http://localhost:8000/notes con un JSON como:
    {
        "title": "Mi primera nota",
        "content": "Contenido de la nota"
    }
    
    Si estás usando curl:
    curl -X POST http://localhost:8000/notes -H "Content-Type: application/json" \
         -d '{"title":"Mi primera nota","content":"Contenido de la nota"}'
    """
    try:
        # Procesamos los datos que nos envía el usuario
        data = await request.json()
        
        # Validamos los datos usando Pydantic para asegurar que cumplen con nuestro esquema
        note_data = NoteCreate(title=data.get("title"), content=data.get("content"))
        
        # No permitimos campos vacíos (solo espacios)
        if not note_data.title.strip() or not note_data.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título y el contenido no pueden estar vacíos"
            )
        
        # Creamos la nota en la base de datos
        db_note = NoteModel(title=note_data.title, content=note_data.content)
        db.add(db_note)
        db.commit()  # Guardamos los cambios
        db.refresh(db_note)  # Actualizamos para obtener el ID asignado
        
        return db_note
    except SQLAlchemyError as e:
        # Si algo sale mal, deshacemos los cambios en la base de datos
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )
    except ValueError as e:
        # Errores de validación (por ejemplo, si faltan campos)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

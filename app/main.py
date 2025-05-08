from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import json
import os

from .database import get_db, Note as NoteModel
from .schemas import Note, NoteCreate

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }


@app.get("/notes", response_model=list[Note])
async def get_notes(db: Session = Depends(get_db)):
    try:
        notes = db.query(NoteModel).all()
        return notes
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(request: Request, db: Session = Depends(get_db)):
    try:
        # Parse the request body
        data = await request.json()
        
        # Validate the data with Pydantic
        note_data = NoteCreate(title=data.get("title"), content=data.get("content"))
        
        # Check for empty fields
        if not note_data.title.strip() or not note_data.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title and content cannot be empty"
            )
        
        # Create a new note
        db_note = NoteModel(title=note_data.title, content=note_data.content)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

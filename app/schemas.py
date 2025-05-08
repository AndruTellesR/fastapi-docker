from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the note")
    content: str = Field(..., min_length=1, description="The content of the note")


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

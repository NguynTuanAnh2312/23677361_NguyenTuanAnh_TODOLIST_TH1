from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class ToDoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None  # list tên tag


class ToDoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class ToDoPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class ToDoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    due_date: Optional[datetime] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ToDoListResponse(BaseModel):
    items: List[ToDoOut]
    total: int
    limit: int
    offset: int
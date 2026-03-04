from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.todo_repo import ToDoRepository
from app.schemas.todo import ToDoCreate, ToDoListResponse, ToDoOut, ToDoPatch, ToDoUpdate
from app.services.todo_service import ToDoService

router = APIRouter(prefix="/todos", tags=["todos"])

_repo = ToDoRepository()
_service = ToDoService(_repo)


def _get_or_404(db: Session, todo_id: int):
    todo = _service.get(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("", response_model=ToDoOut, status_code=201)
def create_todo(payload: ToDoCreate, db: Session = Depends(get_db)):
    return _service.create(db, payload)


@router.get("", response_model=ToDoListResponse)
def list_todos(
    db: Session = Depends(get_db),
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Literal["created_at", "-created_at"] = "created_at",
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return _service.list(db, limit=limit, offset=offset, is_done=is_done, q=q, sort=sort)


@router.get("/{todo_id}", response_model=ToDoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, todo_id)


@router.put("/{todo_id}", response_model=ToDoOut)
def replace_todo(todo_id: int, payload: ToDoUpdate, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    return _service.replace(db, todo, payload)


@router.patch("/{todo_id}", response_model=ToDoOut)
def patch_todo(todo_id: int, payload: ToDoPatch, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    return _service.patch(db, todo, payload)


@router.post("/{todo_id}/complete", response_model=ToDoOut)
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    return _service.complete(db, todo)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = _get_or_404(db, todo_id)
    _service.delete(db, todo)
    return None
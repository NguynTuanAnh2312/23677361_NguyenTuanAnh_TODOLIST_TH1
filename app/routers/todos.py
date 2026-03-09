from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.todo import ToDo
from app.models.user import User
from app.repositories.tag_repo import TagRepository
from app.repositories.todo_repo import ToDoRepository
from app.schemas.todo import ToDoCreate, ToDoListResponse, ToDoOut, ToDoPatch, ToDoUpdate
from app.services.todo_service import ToDoService

router = APIRouter(prefix="/todos", tags=["todos"])

_repo = ToDoRepository()
_tag_repo = TagRepository()
_service = ToDoService(_repo, _tag_repo)


def _get_model_or_404(db: Session, todo_id: int, owner_id: int) -> ToDo:
    todo = _service.get_model(db, todo_id, owner_id=owner_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("", response_model=ToDoOut, status_code=201)
def create_todo(
    payload: ToDoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service.create(db, payload, owner_id=current_user.id)


@router.get("", response_model=ToDoListResponse)
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    is_done: Optional[bool] = None,
    q: Optional[str] = None,
    sort: Literal["created_at", "-created_at"] = "created_at",
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return _service.list(
        db,
        owner_id=current_user.id,
        limit=limit,
        offset=offset,
        is_done=is_done,
        q=q,
        sort=sort,
    )


@router.get("/overdue", response_model=ToDoListResponse)
def overdue_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return _service.overdue(db, owner_id=current_user.id, limit=limit, offset=offset)


@router.get("/today", response_model=ToDoListResponse)
def today_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return _service.today(db, owner_id=current_user.id, limit=limit, offset=offset)


@router.get("/{todo_id}", response_model=ToDoOut)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = _service.get(db, todo_id, owner_id=current_user.id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=ToDoOut)
def replace_todo(
    todo_id: int,
    payload: ToDoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = _get_model_or_404(db, todo_id, owner_id=current_user.id)
    return _service.replace(db, todo, payload, owner_id=current_user.id)


@router.patch("/{todo_id}", response_model=ToDoOut)
def patch_todo(
    todo_id: int,
    payload: ToDoPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = _get_model_or_404(db, todo_id, owner_id=current_user.id)
    return _service.patch(db, todo, payload, owner_id=current_user.id)


@router.post("/{todo_id}/complete", response_model=ToDoOut)
def complete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = _get_model_or_404(db, todo_id, owner_id=current_user.id)
    return _service.complete(db, todo)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = _get_model_or_404(db, todo_id, owner_id=current_user.id)
    _service.delete(db, todo)
    return None
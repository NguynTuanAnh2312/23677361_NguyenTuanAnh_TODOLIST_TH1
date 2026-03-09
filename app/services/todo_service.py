from typing import Literal, Optional

from sqlalchemy.orm import Session

from app.models.todo import ToDo
from app.repositories.tag_repo import TagRepository
from app.repositories.todo_repo import ToDoRepository
from app.schemas.todo import ToDoCreate, ToDoListResponse, ToDoOut, ToDoPatch, ToDoUpdate


def _to_out(todo: ToDo) -> ToDoOut:
    return ToDoOut(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_done=todo.is_done,
        due_date=todo.due_date,
        tags=[t.name for t in (todo.tags or [])],
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


class ToDoService:
    def __init__(self, repo: ToDoRepository, tag_repo: TagRepository) -> None:
        self.repo = repo
        self.tag_repo = tag_repo

    def create(self, db: Session, payload: ToDoCreate, owner_id: int) -> ToDoOut:
        tags = self.tag_repo.get_or_create_many(db, owner_id=owner_id, names=payload.tags or [])
        todo = self.repo.create(db, payload, owner_id, tags)
        return _to_out(todo)

    # NEW: return ORM model (used for delete/patch/put/complete)
    def get_model(self, db: Session, todo_id: int, owner_id: int) -> Optional[ToDo]:
        return self.repo.get_by_id(db, todo_id, owner_id)

    def get(self, db: Session, todo_id: int, owner_id: int) -> Optional[ToDoOut]:
        todo = self.repo.get_by_id(db, todo_id, owner_id)
        return _to_out(todo) if todo else None

    def delete(self, db: Session, todo: ToDo) -> None:
        self.repo.delete(db, todo)

    def replace(self, db: Session, todo: ToDo, payload: ToDoUpdate, owner_id: int) -> ToDoOut:
        tags = self.tag_repo.get_or_create_many(db, owner_id=owner_id, names=payload.tags or [])
        todo = self.repo.replace(db, todo, payload, tags)
        return _to_out(todo)

    def patch(self, db: Session, todo: ToDo, payload: ToDoPatch, owner_id: int) -> ToDoOut:
        tags = None
        if payload.tags is not None:
            tags = self.tag_repo.get_or_create_many(db, owner_id=owner_id, names=payload.tags)
        todo = self.repo.patch(db, todo, payload, tags)
        return _to_out(todo)

    def complete(self, db: Session, todo: ToDo) -> ToDoOut:
        todo = self.repo.complete(db, todo)
        return _to_out(todo)

    def list(
        self,
        db: Session,
        *,
        owner_id: int,
        limit: int,
        offset: int,
        is_done: Optional[bool],
        q: Optional[str],
        sort: Literal["created_at", "-created_at"],
    ) -> ToDoListResponse:
        items, total = self.repo.list(
            db, owner_id=owner_id, limit=limit, offset=offset, is_done=is_done, q=q, sort=sort
        )
        return ToDoListResponse(
            items=[_to_out(t) for t in items],
            total=total,
            limit=limit,
            offset=offset,
        )

    def overdue(self, db: Session, *, owner_id: int, limit: int, offset: int) -> ToDoListResponse:
        items, total = self.repo.list_overdue(db, owner_id=owner_id, limit=limit, offset=offset)
        return ToDoListResponse(items=[_to_out(t) for t in items], total=total, limit=limit, offset=offset)

    def today(self, db: Session, *, owner_id: int, limit: int, offset: int) -> ToDoListResponse:
        items, total = self.repo.list_today(db, owner_id=owner_id, limit=limit, offset=offset)
        return ToDoListResponse(items=[_to_out(t) for t in items], total=total, limit=limit, offset=offset)
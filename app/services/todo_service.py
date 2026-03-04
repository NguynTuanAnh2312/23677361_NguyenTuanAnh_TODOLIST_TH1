from typing import Literal, Optional

from sqlalchemy.orm import Session

from app.repositories.todo_repo import ToDoRepository
from app.schemas.todo import ToDoCreate, ToDoListResponse, ToDoPatch, ToDoUpdate


class ToDoService:
    def __init__(self, repo: ToDoRepository) -> None:
        self.repo = repo

    def create(self, db: Session, payload: ToDoCreate):
        return self.repo.create(db, payload)

    def get(self, db: Session, todo_id: int):
        return self.repo.get_by_id(db, todo_id)

    def delete(self, db: Session, todo) -> None:
        self.repo.delete(db, todo)

    def replace(self, db: Session, todo, payload: ToDoUpdate):
        return self.repo.replace(db, todo, payload)

    def patch(self, db: Session, todo, payload: ToDoPatch):
        return self.repo.patch(db, todo, payload)

    def complete(self, db: Session, todo):
        return self.repo.complete(db, todo)

    def list(
        self,
        db: Session,
        *,
        limit: int,
        offset: int,
        is_done: Optional[bool],
        q: Optional[str],
        sort: Literal["created_at", "-created_at"],
    ) -> ToDoListResponse:
        items, total = self.repo.list(
            db, limit=limit, offset=offset, is_done=is_done, q=q, sort=sort
        )
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)
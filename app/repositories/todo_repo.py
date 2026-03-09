from datetime import datetime, timedelta, timezone
from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.todo import ToDo
from app.models.tag import Tag
from app.schemas.todo import ToDoCreate, ToDoPatch, ToDoUpdate


class ToDoRepository:
    def create(self, db: Session, payload: ToDoCreate, owner_id: int, tags: Sequence[Tag]) -> ToDo:
        todo = ToDo(
            owner_id=owner_id,
            title=payload.title,
            description=payload.description,
            is_done=False,
            due_date=payload.due_date,
        )
        todo.tags = list(tags)

        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_by_id(self, db: Session, todo_id: int, owner_id: int) -> Optional[ToDo]:
        stmt = select(ToDo).where(ToDo.id == todo_id, ToDo.owner_id == owner_id)
        return db.execute(stmt).scalar_one_or_none()

    def delete(self, db: Session, todo: ToDo) -> None:
        db.delete(todo)
        db.commit()

    def replace(self, db: Session, todo: ToDo, payload: ToDoUpdate, tags: Sequence[Tag]) -> ToDo:
        todo.title = payload.title
        todo.description = payload.description
        todo.is_done = payload.is_done
        todo.due_date = payload.due_date
        todo.tags = list(tags)

        db.commit()
        db.refresh(todo)
        return todo

    def patch(self, db: Session, todo: ToDo, payload: ToDoPatch, tags: Optional[Sequence[Tag]]) -> ToDo:
        data = payload.model_dump(exclude_unset=True)

        if "title" in data:
            todo.title = data["title"]
        if "description" in data:
            todo.description = data["description"]
        if "is_done" in data:
            todo.is_done = data["is_done"]
        if "due_date" in data:
            todo.due_date = data["due_date"]

        # tags only update when client sends tags field
        if tags is not None:
            todo.tags = list(tags)

        db.commit()
        db.refresh(todo)
        return todo

    def complete(self, db: Session, todo: ToDo) -> ToDo:
        todo.is_done = True
        db.commit()
        db.refresh(todo)
        return todo

    def list(
        self,
        db: Session,
        *,
        owner_id: int,
        limit: int,
        offset: int,
        is_done: Optional[bool],
        q: Optional[str],
        sort: str,
    ) -> tuple[Sequence[ToDo], int]:
        stmt = select(ToDo).where(ToDo.owner_id == owner_id)

        if is_done is not None:
            stmt = stmt.where(ToDo.is_done == is_done)

        if q:
            stmt = stmt.where(ToDo.title.ilike(f"%{q.strip()}%"))

        if sort == "-created_at":
            stmt = stmt.order_by(ToDo.created_at.desc())
        else:
            stmt = stmt.order_by(ToDo.created_at.asc())

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.execute(total_stmt).scalar_one()

        items = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return items, total

    def list_overdue(self, db: Session, *, owner_id: int, limit: int, offset: int):
        now = datetime.now(timezone.utc)
        stmt = (
            select(ToDo)
            .where(
                ToDo.owner_id == owner_id,
                ToDo.is_done == False,  # noqa: E712
                ToDo.due_date.is_not(None),
                ToDo.due_date < now,
            )
            .order_by(ToDo.due_date.asc())
        )
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.execute(total_stmt).scalar_one()
        items = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return items, total

    def list_today(self, db: Session, *, owner_id: int, limit: int, offset: int):
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        stmt = (
            select(ToDo)
            .where(
                ToDo.owner_id == owner_id,
                ToDo.due_date.is_not(None),
                ToDo.due_date >= start,
                ToDo.due_date < end,
            )
            .order_by(ToDo.due_date.asc())
        )
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.execute(total_stmt).scalar_one()
        items = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return items, total
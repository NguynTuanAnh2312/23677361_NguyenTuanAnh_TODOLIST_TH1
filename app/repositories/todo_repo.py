from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.todo import ToDo
from app.schemas.todo import ToDoCreate, ToDoPatch, ToDoUpdate


class ToDoRepository:
    def create(self, db: Session, payload: ToDoCreate) -> ToDo:
        todo = ToDo(
            title=payload.title,
            description=payload.description,
            is_done=False,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_by_id(self, db: Session, todo_id: int, owner_id: int) -> Optional[ToDo]:
        return db.execute(
            select(ToDo).where(ToDo.id == todo_id, ToDo.owner_id == owner_id)
    ).scalar_one_or_none()

    def delete(self, db: Session, todo: ToDo) -> None:
        db.delete(todo)
        db.commit()

    def replace(self, db: Session, todo: ToDo, payload: ToDoUpdate) -> ToDo:
        todo.title = payload.title
        todo.description = payload.description
        todo.is_done = payload.is_done
        db.commit()
        db.refresh(todo)
        return todo

    def patch(self, db: Session, todo: ToDo, payload: ToDoPatch) -> ToDo:
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(todo, k, v)
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
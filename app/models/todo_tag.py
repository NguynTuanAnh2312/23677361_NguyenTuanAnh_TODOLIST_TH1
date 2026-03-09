from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ToDoTag(Base):
    __tablename__ = "todo_tags"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
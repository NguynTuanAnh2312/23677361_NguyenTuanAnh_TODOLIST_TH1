# Ensure models are importable for Alembic autogenerate
from app.models.todo import ToDo  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.tag import Tag  # noqa: F401
from app.models.todo_tag import ToDoTag  # noqa: F401
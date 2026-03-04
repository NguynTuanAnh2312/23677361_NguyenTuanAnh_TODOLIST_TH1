"""init users and todos

Revision ID: 23e41a67fd2e
Revises: d138061fd685
Create Date: 2026-03-04 23:46:28.425215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "23e41a67fd2e"
down_revision: Union[str, Sequence[str], None] = "d138061fd685"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1) Create users table (OK on SQLite)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # 2) Alter todos table with SQLite batch mode (required for FK/constraints)
    with op.batch_alter_table("todos", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=False))
        batch_op.create_index(op.f("ix_todos_owner_id"), ["owner_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_todos_owner_id_users",
            "users",
            ["owner_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    # 1) Revert todos table changes using batch mode
    with op.batch_alter_table("todos", recreate="always") as batch_op:
        batch_op.drop_constraint("fk_todos_owner_id_users", type_="foreignkey")
        batch_op.drop_index(op.f("ix_todos_owner_id"))
        batch_op.drop_column("owner_id")

    # 2) Drop users table
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
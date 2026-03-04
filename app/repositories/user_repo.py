from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    def create(self, db: Session, *, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password, is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
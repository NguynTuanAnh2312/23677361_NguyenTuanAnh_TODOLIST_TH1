from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def register(self, db: Session, *, email: str, password: str) -> User:
        existed = self.user_repo.get_by_email(db, email)
        if existed:
            raise ValueError("Email already registered")

        user = self.user_repo.create(db, email=email, hashed_password=hash_password(password))
        return user

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.user_repo.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user
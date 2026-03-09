from typing import Iterable, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def get_or_create_many(self, db: Session, *, owner_id: int, names: Iterable[str]) -> List[Tag]:
        cleaned = []
        for n in names:
            n = (n or "").strip().lower()
            if n:
                cleaned.append(n)

        unique_names = sorted(set(cleaned))
        if not unique_names:
            return []

        existing = db.execute(
            select(Tag).where(Tag.owner_id == owner_id, Tag.name.in_(unique_names))
        ).scalars().all()

        existing_map = {t.name: t for t in existing}
        result: List[Tag] = list(existing)

        for name in unique_names:
            if name not in existing_map:
                tag = Tag(owner_id=owner_id, name=name)
                db.add(tag)
                result.append(tag)

        db.commit()
        # refresh không bắt buộc vì relationship dùng id sau commit là OK
        return result
from sqlalchemy import Column, DateTime, Integer, String, func

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"User(id={self.id}, email='{self.email}')"

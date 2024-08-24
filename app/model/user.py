from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from app.schemas.ReadORM.read_user import ReadUSerModel
from .base import Base
class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    in_match: Mapped[bool] = mapped_column(default=False)
    doc: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_read_model(self) -> ReadUSerModel:
        return ReadUSerModel(
        username = self.username,
        password = self.password,
        email = self.email,
        in_match = self.in_match,
        )
            




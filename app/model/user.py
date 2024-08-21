from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime , timezone
from app.schemas.ReadORM.read_user import ReadUSerModel
class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    doc: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    in_match: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> ReadUSerModel:
        return ReadUSerModel(
        username = self.username,
        password = self.password,
        email = self.email,
        doc = self.doc,
        in_match = self.in_match,
        )
            




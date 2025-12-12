from datetime import datetime, timedelta

from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.model.base import Base

from app.schemas.ReadORM.read_user import ReadUserModel


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    doc: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)  # дата создания
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Связь с корзиной
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="user")

    @classmethod
    async def delete_unverified_users(cls, session):
        """
        Удаляет всех пользователей, которые не подтвердили свою учетную запись в течение 7 дней.
        """
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        unverified_users = session.query(cls).filter(cls.is_verified == False,
                                                     cls.created_at <= seven_days_ago).all()
        for user in unverified_users:
            session.delete(user)
        await session.commit()

    def to_read_model(self) -> ReadUserModel:
        """
        Преобразует объект пользователя в ReadUserModel
        """
        return ReadUserModel(
            id=self.id,
            name=self.name,
            lastname=self.lastname,
            email=self.email,
            password=self.password,
            doc=self.doc,
            is_verified=self.is_verified
        )





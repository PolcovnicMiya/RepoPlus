from datetime import datetime, timedelta

from sqlalchemy import BigInteger, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base

from app.schemas.ReadORM.read_user import ReadUserModel


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    card_number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    photo: Mapped[str] = mapped_column(nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    role: Mapped[int] = mapped_column(default=0)

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
        Преобразует объект пользователя в ReadUserMode
        """
        return ReadUserModel(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            name=self.name,
            lastname=self.lastname,
            card_number=self.card_number,
            balance=self.balance,
            photo=self.photo,
            is_verified=self.is_verified
        )





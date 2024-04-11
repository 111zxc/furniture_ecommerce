from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(server_default="user")
    email: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted: Mapped[bool] = mapped_column(server_default=False)

    passwords = relationship("Password", back_populates="user")

class Password(Base):
    __tablename__ = 'passwords'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    md5_password: Mapped[str] = mapped_column()
    sha256_password: Mapped[str] = mapped_column()

    user = relationship("User", back_populates="password")
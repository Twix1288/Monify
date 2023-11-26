from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column, declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    goals_notes: Mapped[List["Goals_Notes"]] = relationship(back_populates='user')
    finances: Mapped["FinanceInfo"] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"<User username={self.username}>"


class FinanceInfo(Base):
    __tablename__ = 'FinanceInfo'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users'))
    total_amount: Mapped[int] = mapped_column(nullable=False)
    choice_gen: Mapped[int] = mapped_column(nullable=False)
    allowance: Mapped[int] = mapped_column(nullable=False)
    income: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship(back_populates='finances')

    def __repr__(self) -> str:
        return (f"<User total_amount={self.total_amount} allowance={self.allowance} income={self.income} made all by "
                f"user={self.user.username}>")


class Goals_Notes(Base):
    __tablename__ = 'Goals_Notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users'))
    note: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["Users"] = relationship(back_populates='goals_notes')

    def __repr__(self) -> str:
        return f"<User note={self.note} made all by user={self.user.username}>"

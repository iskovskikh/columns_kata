from sqlalchemy import MetaData, func, select
from sqlalchemy.orm import DeclarativeBase, column_property, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData()


class SimpleModel(Base):
    __tablename__ = 'simple'

    oid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    is_simple = column_property(
        select(func.true()).scalar_subquery()
    )

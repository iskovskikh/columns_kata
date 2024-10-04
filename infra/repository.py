from dataclasses import dataclass
from typing import Callable

from sqlalchemy import Executable, Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.models import SimpleModel


@dataclass
class SimpleRepository():
    session_maker: Callable[[], AsyncSession]

    async def add_simple(self, simple_model: SimpleModel) -> int:
        async with self.session_maker() as session:
            session.add(simple_model)
            await session.commit()

            # Если пытаться читать `simple_model.is_simple`, то возникает ошибка:
            # > sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called;
            # > can't call await_only() here. Was IO attempted in an unexpected place?
            # > (Background on this error at: https://sqlalche.me/e/20/xd2s)

            print(f'>>>{simple_model.oid}')
            print(f'>>>{simple_model.title}')
            # print(f'>>>{simple_model.is_simple}')

            return simple_model.oid

    async def get_simple_by_oid(self, simple_oid: int) -> SimpleModel | None:
        async with self.session_maker() as session:
            statement: Executable = select(SimpleModel).where(SimpleModel.oid == simple_oid)
            result: Result = await session.execute(statement)
            return result.scalars().one_or_none()

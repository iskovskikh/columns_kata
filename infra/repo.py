from dataclasses import dataclass
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from infra.models import SimpleModel


@dataclass
class SimpleRepository():
    session_maker: Callable[[], AsyncSession]

    async def simple_add(self, simple_model: SimpleModel):

        async with self.session_maker() as session:
            session.add(simple_model)
            await session.commit()

            print(f'>>>{simple_model.oid}')
            print(f'>>>{simple_model.title}')
            print(f'>>>{simple_model.is_simple}')


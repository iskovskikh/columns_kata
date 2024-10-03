import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from infra.models import SimpleModel, Base
from infra.repo import SimpleRepository


# @pytest.fixture(scope='session')
# def session_maker(create_postgresql_session_maker):
#     with PostgresContainer(username='test_user', dbname='test_db') as postgres:
#         url = postgres.get_connection_url(driver='asyncpg')
#         yield create_postgresql_session_maker(db_url=url)


@pytest.fixture(scope='session')
def postgresql_container_url():
    with PostgresContainer(username='test_user', dbname='test_db') as postgres:
        url = postgres.get_connection_url(driver='asyncpg')
        yield url


@pytest.fixture(scope='session')
def engine(postgresql_container_url):
    engine: AsyncEngine = create_async_engine(url=postgresql_container_url, echo=True)
    return engine


@pytest.fixture(scope='session')
def session_maker(engine):
    session_maker = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return session_maker


@pytest.fixture
async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio(loop_scope='session')
async def test_simple_add(session_maker, init_db):
    async for db in init_db:

        simple: SimpleModel = SimpleModel(title='simple title')

        simple_repository: SimpleRepository = SimpleRepository(session_maker=session_maker)
        await simple_repository.simple_add(simple_model=simple)

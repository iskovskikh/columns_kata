import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from infra.models import SimpleModel, Base
from infra.repository import SimpleRepository


@pytest.fixture(scope='session')
# @pytest.fixture()
def postgresql_container_url():
    with PostgresContainer(username='test_user', dbname='test_db') as postgres:
        url = postgres.get_connection_url(driver='asyncpg')
        yield url


@pytest.fixture(scope='session')
# @pytest.fixture()
def engine(postgresql_container_url):
    engine: AsyncEngine = create_async_engine(url=postgresql_container_url, echo=True)
    return engine


@pytest.fixture(scope='session')
# @pytest.fixture()
def session_maker(engine):
    session_maker = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    # session_maker = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)
    return session_maker


# @pytest.fixture(scope='session')
@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def init_db(engine, ):
    print('>>> create_all')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print('>>> drop_all')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio(loop_scope='session')
async def test_simple_add(session_maker, init_db):
    simple: SimpleModel = SimpleModel(title='simple title 1')

    simple_repository: SimpleRepository = SimpleRepository(session_maker=session_maker)
    await simple_repository.add_simple(simple_model=simple)

    saved_simple: SimpleModel = await simple_repository.get_simple_by_oid(simple_oid=simple.oid)

    assert saved_simple
    assert saved_simple.oid == 1
    assert saved_simple.title == simple.title
    assert saved_simple.is_simple == 42


@pytest.mark.asyncio(loop_scope='session')
async def test_simple_add_again(session_maker, init_db):
    simple: SimpleModel = SimpleModel(title='simple title 2')

    simple_repository: SimpleRepository = SimpleRepository(session_maker=session_maker)
    simple_oid = await simple_repository.add_simple(simple_model=simple)

    assert simple.oid == simple_oid

    saved_simple: SimpleModel = await simple_repository.get_simple_by_oid(simple_oid=simple_oid)

    assert saved_simple
    assert saved_simple.oid == 2
    assert saved_simple.title == simple.title
    assert saved_simple.is_simple == 42

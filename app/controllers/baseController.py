import json
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import DATABASE_URL


class PGSClient:
    _engine = None
    _sessionmaker = None
    _DATABASE_URL = DATABASE_URL

    @classmethod
    async def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_async_engine(
                cls._DATABASE_URL,
                pool_size=50,
                max_overflow=10,
                pool_timeout=5,
                pool_recycle=300,
                pool_pre_ping=True,
                echo=False
            )
        return cls._engine

    @classmethod
    async def get_session(cls):
        if cls._sessionmaker is None:
            engine = await cls.get_engine()
            cls._sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
        return cls._sessionmaker

    async def __aenter__(self):
        sessionmaker = await self.get_session()
        self._session = sessionmaker()
        return self._session

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        if self.redis is None:
            self.redis = redis.Redis(host='localhost', port=6379, db=0)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def set_data(self, key, data, expire=None):
        await self.redis.set(key, json.dumps(data), ex=expire)

    async def get_data(self, key):
        data = await self.redis.get(key)
        if data is not None:
            if not isinstance(data, bool):
                return json.loads(data)
            else:
                return data
        return None

    @staticmethod
    async def row_to_dict(row):
        return {column: value for column, value in row._mapping.items()}

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

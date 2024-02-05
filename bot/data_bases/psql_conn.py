import asyncpg

from bot.config import db_user, db_password


class DB_conn:
    def __init__(self):
        self.database = 'ozflowers'
        self.user = db_user
        self.password = db_password
        self.host = 'localhost'
        self.port = 5433
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

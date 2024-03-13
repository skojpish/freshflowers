import asyncpg

from bot.config import db_user, db_password, db_name, db_host, db_port


class DB_conn:
    def __init__(self):
        self.database = db_name
        self.user = db_user
        self.password = db_password
        self.host = db_host
        self.port = db_port
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

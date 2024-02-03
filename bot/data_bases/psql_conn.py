import asyncpg

class DB_conn:
    def __init__(self):
        self.database = 'ozflowers'
        self.user = 'postgres'
        self.password = 'root'
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

from bot.data_bases.psql_conn import DB_conn
from .config_logger_db import logger

class DB_basket(DB_conn):
    async def create_basket_table(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute('''CREATE TABLE IF NOT EXISTS users_basket (id SERIAL PRIMARY KEY,
                                                       user_id INTEGER NULL,
                                                       item TEXT NULL,
                                                       count INTEGER NULL,
                                                       pre_order_data TEXT NULL,
                                                       category TEXT NULL);''')
        except Exception as e:
            logger.error(e)

    async def add_user_to_stat(self, user_id, username):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        f"INSERT INTO statistic_user (user_id, username) SELECT $1, $2 "
                        f"WHERE NOT EXISTS (SELECT * FROM statistic_user WHERE user_id = $1);", user_id, username)
        except Exception as e:
            logger.error(e)

    async def get_all_users(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    users = await conn.fetch(
                        f"SELECT user_id FROM statistic_user;")
        except Exception as e:
            logger.error(e)
        else:
            return users

    async def add_item_to_basket(self, user, item, cat):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"INSERT INTO users_basket (user_id, item, category) SELECT $1, $2, $3 "
                                       f"WHERE NOT EXISTS (SELECT * FROM users_basket WHERE user_id = $1 AND item=$2 "
                                       f"AND category=$3);", user, item, cat)
        except Exception as e:
            logger.error(e)

    async def add_pre_order_to_basket(self, user, pre_order):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"INSERT INTO users_basket (user_id, pre_order_data) SELECT $1, $2 "
                                       f"WHERE NOT EXISTS (SELECT * FROM users_basket WHERE user_id = $1 "
                                       f"AND pre_order_data IS NOT NULL);", user, pre_order)
        except Exception as e:
            logger.error(e)

    async def add_items_count(self, count, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE users_basket SET count=$1 WHERE count IS NULL AND user_id=$2;",
                                       count, user)
        except Exception as e:
            logger.error(e)

    async def set_count_null(self, name, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE users_basket SET count=NULL WHERE item = $1 AND user_id = $2;",
                                       name, user)
        except Exception as e:
            logger.error(e)

    async def print_basket(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM users_basket WHERE user_id = $1;", user)
        except Exception as e:
            logger.error(e)
        else:
            return rows

    async def delete_user_basket(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM users_basket WHERE user_id = $1;", user)
        except Exception as e:
            logger.error(e)

    async def delete_item(self, name, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM users_basket WHERE item = $1 AND user_id = $2;", name, user)
        except Exception as e:
            logger.error(e)

    async def delete_item_if_null(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM users_basket WHERE count IS NULL AND pre_order_data IS NULL AND "
                                       f"user_id = $1;", user)
        except Exception as e:
            logger.error(e)

    async def delete_pre_ord(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM users_basket WHERE pre_order_data IS NOT NULL AND user_id=$1;",
                                       user)
        except Exception as e:
            logger.error(e)

    async def update_pre_order(self, pre_ord, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE users_basket SET pre_order_data=$1 WHERE pre_order_data IS NOT NULL"
                                       f" AND user_id=$2;", pre_ord, user)
        except Exception as e:
            logger.error(e)

    async def get_name_item_where_null(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM users_basket WHERE count IS NULL AND pre_order_data"
                                              f" IS NULL AND user_id=$1;", user)
                    name = row[2]
        except Exception as e:
            logger.error(e)
        else:
            return name


db_basket = DB_basket()

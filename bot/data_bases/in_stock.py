from bot.data_bases.psql_conn import DB_conn
from .config_logger_db import logger

class DB_inst(DB_conn):
    async def get_category_data10(self, category):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_instock WHERE category=$1 AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10;", category)
        except Exception as e:
            logger.error(e)
        else:
            return rows

    async def get_category_data_more(self, category, offset):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_instock WHERE category=$1 AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10 OFFSET $2;",
                                            category, offset)
        except Exception as e:
            logger.error(e)
        else:
            return rows

    async def get_specific_row(self, item_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE id=$1;", item_id)
        except Exception as e:
            logger.error(e)
        else:
            return row

    async def get_categories(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    data = await conn.fetch(f"SELECT category FROM administration_instock WHERE photo!='' "
                                            f"OR image_id!='';")
                    categories = []
                    for i in range(len(data)):
                        if data[i][0] in categories:
                            pass
                        else:
                            categories.append(data[i][0])
        except Exception as e:
            logger.error(e)
        else:
            return categories

    async def add_image_id(self, item_id, image_id, name_image_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_instock SET image_id=$1, "
                                       f"name_image_id=$2 WHERE id=$3;",
                                       image_id, name_image_id, item_id)
        except Exception as e:
            logger.error(e)

    async def change_col(self, col, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_instock SET col=col-$1 WHERE name=$2;", col, name)
        except Exception as e:
            logger.error(e)

    async def delete_item(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM administration_instock WHERE col=0;")
        except Exception as e:
            logger.error(e)

    async def get_row_by_name(self, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE name=$1;", name)
        except Exception as e:
            logger.error(e)
        else:
            return row


db_inst = DB_inst()

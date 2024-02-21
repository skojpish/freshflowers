from bot.data_bases.psql_conn import DB_conn
from .config_logger_db import logger

class DB_otw(DB_conn):
    async def get_category_data10(self, category):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM administration_item WHERE category='{category}' AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10;")
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
                    rows = await conn.fetch(f"SELECT * FROM administration_item WHERE category='{category}' AND "
                                            f"(photo!='' OR image_id IS NOT NULL) ORDER BY id LIMIT 10 OFFSET {offset};")
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
                    row = await conn.fetchrow(f"SELECT * FROM administration_item WHERE id={item_id};")
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
                    data = await conn.fetch(f"SELECT category FROM administration_item WHERE photo!='' OR image_id!='';")
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
                    await conn.execute(f"UPDATE administration_item SET image_id='{image_id}', "
                                       f"name_image_id='{name_image_id}' WHERE id='{item_id}';")
        except Exception as e:
            logger.error(e)

    async def change_col(self, col, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE administration_item SET col=col-{col} WHERE name=$1;", name)
        except Exception as e:
            logger.error(e)

    async def delete_item(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM administration_item WHERE col=0;")
        except Exception as e:
            logger.error(e)

    async def get_row_by_name(self, name):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_item WHERE name=$1;", name)
        except Exception as e:
            logger.error(e)
        else:
            return row

    async def check_date(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"INSERT INTO administration_instock SELECT * FROM administration_item WHERE item_date < LOCALTIMESTAMP;")
                    await conn.execute(f"DELETE FROM administration_item WHERE item_date < LOCALTIMESTAMP;")
        except Exception as e:
            logger.error(e)


db_otw = DB_otw()

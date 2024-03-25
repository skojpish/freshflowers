from bot.data_bases.psql_conn import DB_conn
from .config_logger_db import logger


class DBImagesId(DB_conn):
    async def add_image_otw(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_item WHERE col=0;")
                    if row is not None:
                        await conn.execute(f"INSERT INTO administration_telegramidimage (name, id_image) "
                                           f"VALUES ($1, $2);", row[1], row[10])
        except Exception as e:
            logger.error(e)

    async def add_image_inst(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM administration_instock WHERE col=0;")
                    if row is not None:
                        await conn.execute(f"INSERT INTO administration_telegramidimage (name, id_image) "
                                           f"VALUES ($1, $2);", row[1], row[10])
                    else:
                        pass
        except Exception as e:
            logger.error(e)


db_tg_image = DBImagesId()

from bot.data_bases.psql_conn import DB_conn

class DB_order(DB_conn):
    async def create_order_table(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute('''CREATE TABLE IF NOT EXISTS user_order (id SERIAL PRIMARY KEY,
                                                       user_id INTEGER NULL,
                                                       business_type TEXT NULL,
                                                       full_name TEXT NULL,
                                                       number TEXT NULL);''')
        except:
            print("MDA")

    async def add_user_to_order(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        f"INSERT INTO user_order (user_id) SELECT {user} WHERE NOT EXISTS (SELECT * FROM user_order WHERE user_id = {user});")
        except:
            print("MDA")

    async def add_bus_type(self, user, bus_type):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET business_type='{bus_type}' WHERE user_id = {user};")
        except:
            print("MDA")

    async def add_full_name(self, user, fname):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET full_name='{fname}' WHERE user_id = {user};")
        except:
            print("MDA")

    async def add_number(self, user, number):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET number={number} WHERE user_id = {user};")
        except:
            print('MDA')

    async def get_ord_row(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM user_order WHERE user_id = {user};")
        except:
            print('MDA')
        else:
            return row

    async def delete_user_data(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"DELETE FROM user_order WHERE user_id = {user};")
        except:
            print("MDA")

    async def add_order_to_site(self, user_name, link, order, type_of_b, fullname, number, time):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        f"INSERT INTO statistic_order(user_name, link_user, order_user, type_of_b, fullname, number, time_ord) "
                        f"VALUES('{user_name}', '{link}', $1, '{type_of_b}', '{fullname}', '{number}', '{time}');", order)
        except:
            print("MDA")

db_ord = DB_order()

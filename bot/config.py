from os import getenv
from aiogram import Bot
from dotenv import load_dotenv


load_dotenv('bot/.env')

token = getenv("TOKEN")
bot = Bot(token, parse_mode="HTML")
master_id1 = getenv("MASTER_ID1")
master_username1 = getenv("MASTER_USERNAME1")
master_id2 = getenv("MASTER_ID2")
master_username2 = getenv("MASTER_USERNAME2")
db_user = getenv("DB_USER")
db_password = getenv("DB_PASSWORD")



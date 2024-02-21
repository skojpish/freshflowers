from loguru import logger

logger.add("bot/logs/error_db.log", level="ERROR", rotation="20 MB", compression="zip")
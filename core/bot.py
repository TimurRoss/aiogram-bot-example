from aiogram import Bot
from limited_aiogram import LimitedBot
from aiogram.enums import ParseMode
from core.config import config
from aiogram.client.default import DefaultBotProperties

# Объект бота
bot = LimitedBot(token=config.BOT_TOKEN,
                 default=DefaultBotProperties(
                     parse_mode=ParseMode.MARKDOWN
                 ))

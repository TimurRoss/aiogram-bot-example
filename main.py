import asyncio
from core.tools import functions
from core import config
from core.logger_setup import SetupLogs
from aiogram import Dispatcher,types
from core.bot import bot
from core.handlers import admin_handlers
from core.middleware.apshedulermiddleware import SchedulerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from core.scheduler import SetupScheduler
import logging

SetupLogs()

async def main():

    scheduler = SetupScheduler()

    # Диспетчер
    dp = Dispatcher()


    await bot.set_my_commands([
        types.BotCommand(command="start", description="Запустить/перезагрузить бота"),
    ])


    # Роутеры
    dp.include_routers(admin_handlers.router)
                       #exceptions.router)

    # Мидлевари
    dp.update.middleware(SchedulerMiddleware(scheduler))

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)#,allowed_updates=["message", "callback_query",'message_reaction',])
if __name__ == "__main__":
    asyncio.run(main())
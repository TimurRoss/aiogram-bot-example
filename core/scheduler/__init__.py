from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from core.tools import functions
from .add_start_job import add_job

def SetupScheduler():
    jobstores = {
        'default': RedisJobStore(db=0, jobs_key='notice_bot.keys',
                                 run_times_key='notice_bot.run_times')
    }
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow",
                                 jobstores=jobstores)
    scheduler.start()

    add_job(scheduler=scheduler,
            func=functions.update_statistics,
            id='update_statistics',
            trigger='cron',
            hour=0)
    return scheduler


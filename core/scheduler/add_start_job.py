from apscheduler.triggers.base import BaseTrigger
from apscheduler.util import undefined
from typing import Any
import datetime


def add_job(scheduler,
        func: Any,
        id: str,
        trigger: str | BaseTrigger = None,
        args: list | tuple = None,
        kwargs: dict = None,
        name: str = None,
        misfire_grace_time: int = undefined,
        coalesce: bool = undefined,
        max_instances: int = undefined,
        next_run_time: datetime = undefined,
        jobstore: str = 'default',
        executor: str = 'default',
        replace_existing: bool = False,
        **trigger_args: Any):
    if scheduler.get_job(id) is None:
        scheduler.add_job(func, id, trigger, args, kwargs, name, misfire_grace_time, coalesce, max_instances,
                          next_run_time, jobstore, executor, replace_existing, trigger_args)

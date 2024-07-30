import logging
import logging.handlers
from loguru import logger
import sys

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Получаем соответствующий уровень `Loguru`, если он существует..
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Ищем вызывающего абонента, откуда поступило зарегистрированное сообщение.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
def SetupLogs():
    logging.basicConfig(handlers=[InterceptHandler()],
                        level=0,
                        format="%(asctime)s %(levelname)s %(message)s",
                        force=True)
    logger.remove()
    logger.add(sys.stderr, level='DEBUG', backtrace=False,diagnose=True)
    logger.add("core/logs/log.log",level='DEBUG', rotation="40 MB", retention="10 days", backtrace=False,diagnose =True)




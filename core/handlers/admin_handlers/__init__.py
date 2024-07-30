from core.config import config
from aiogram import F,Router
from core.filters.chat_type import ChatTypeFilter,ChatTypeFilterCallBack
from core.handlers.admin_handlers import foradmin

router = Router()


router.message.filter(F.chat.id.in_(config.ADMIN_IDS),
                      ChatTypeFilter(chat_type=['private']))
router.callback_query.filter(F.message.chat.id.in_(config.ADMIN_IDS),
                             ChatTypeFilterCallBack(chat_type=['private']))
router.message_reaction.filter(F.chat.id.in_(config.ADMIN_IDS),
                               ChatTypeFilter(chat_type=['private']))


router.include_routers(foradmin.router)

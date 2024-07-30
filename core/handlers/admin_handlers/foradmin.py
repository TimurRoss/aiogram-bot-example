from core.keyboards import AdminKeyboards
from aiogram import types, F,Router,md
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.db.mysql_connect import mysql
from aiogram.types import FSInputFile
from core.states import AdminStates
from core.filters.chat_type import ChatTypeFilter,ChatTypeFilterCallBack
import logging
import os
from core import tools,texts
from core.config import config

# logger=Logger()

router = Router()

router.message.filter(ChatTypeFilter(chat_type=["private"]))
router.callback_query.filter(ChatTypeFilterCallBack(chat_type=["private"]))
router.message.filter(F.chat.id.in_(config.ADMIN_IDS))
router.callback_query.filter(F.message.chat.id.in_(config.ADMIN_IDS))


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(
        text=texts.admin.cmd_start,
        reply_markup=AdminKeyboards.cmd_start()
    )

@router.callback_query(F.data == "main_menu")
async def usr_orders_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.message.answer(
        text=texts.admin.usr_main_menu,
        reply_markup=AdminKeyboards.main_menu()
    )


@router.callback_query(F.data.startswith('workers_page_'))
async def clb_list_message_next_last_page(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    user_data=await state.get_data()
    if tools.state_data_is_empty(user_data):
        user_data= tools.create_start_state_data()

    if user_data.get('sort_workers') is None:
        user_data['sort_workers']='count_in_day'

    if callback.data=='workers_page_start':
        user_data['page_list_workers']=1
    if callback.data=='workers_page_next':
        user_data['page_list_workers']+=1
    elif callback.data=='workers_page_last':
        user_data['page_list_workers']-=1

    count = mysql.count_all('workers')

    if count == 0:
        await callback.message.answer(
            text=texts.admin.usr_list_workers_empty,
            reply_markup=AdminKeyboards.page_list_workers_empty()
        )
        return

    max_page = count // 5 + (0 if count % 5 == 0 else 1)
    user_data['page_list_workers'] = tools.constrain(user_data['page_list_workers'],
                                                     min_=1,
                                                     max_=max_page)

    list_message = mysql.search_n('statistics',
                                  step=user_data['page_list_workers'],
                                  count=5,
                                  sort_name=user_data['sort_workers'])
    list_id=[]
    for i in list_message:
        result = mysql.search_n('workers',
                                  login=i[0])
        list_id.append(result[0][0])
    list_message_str = tools.get_string_list_message_workers(list_message)
    await state.update_data(page_list_workers=user_data['page_list_workers'])
    await callback.message.edit_text(
        text=texts.admin.usr_list_workers.format(list=list_message_str),
        reply_markup=AdminKeyboards.page_list_workers(page=user_data['page_list_workers'],
                                                      max_page=max_page,
                                                      count=count,
                                                      list_workers=list_message,
                                                      list_id=list_id)
    )

@router.callback_query(F.data=='choice_worker_sort')
async def clb_list_message_next_last_page(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    user_data=await state.get_data()
    if user_data.get('sort_workers') is None:
        user_data['sort_workers']='count_in_day'
    d = {'count_in_day':'Кол-во обработок (1 день)',
         'count_in_week':'Кол-во обработок (1 неделя)',
         'count_in_month':'Кол-во обработок (текущий месяц)',
         'count_in_last_month':'Кол-во обработок (прошлый месяц)',
         'sum_time_in_day':'Среднее время обработок (1 день)',
         'sum_time_in_week':'Среднее время обработок (1 неделя)',
         'sum_time_in_month':'Среднее время обработок (текущий месяц)',
         'sum_time_in_last_month':'Среднее время обработок (прошлый месяц)'}
    await callback.message.answer(text=texts.admin.choice_worker_sort.format(sort_type=d[user_data['sort_workers']]),
                                  reply_markup=AdminKeyboards.choice_worker_sort())
@router.callback_query(F.data.startswith('choice_worker_sort_'))
async def clb_list_message_next_last_page(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await state.update_data(sort_workers=callback.data[19:])

    await callback.message.answer(text=texts.admin.choice_worker_sort_complete,
                                  reply_markup=AdminKeyboards.choice_worker_sort_complete())


@router.callback_query(F.data.startswith('worker_local_id_'))
async def clb_list_message_next_last_page(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    id = int(callback.data.replace('worker_local_id_',''))
    result=mysql.search_n('workers',id=id)
    worker_login = tools.get_worker_login(result)
    result = mysql.search_n('statistics',count=None, login=worker_login)
    if result == []:
        await callback.message.answer(text=texts.admin.worker_no_have_statistics)
    else:
        result=list(result[0])
        for i in range(1,5):
            if result[i]!=0:
                result[i+4]=round(int(result[i+4])/60/int(result[i]),2)
        await callback.message.answer(text=texts.admin.worker_statistics.format(count_in_day=result[1],
                                                                                     count_in_week=result[2],
                                                                                     count_in_month=result[3],
                                                                                     count_in_last_month=result[4],
                                                                                     mean_time_in_day=result[5],
                                                                                     mean_time_in_week=result[6],
                                                                                     mean_time_in_month=result[7],
                                                                                     mean_time_in_last_month=result[8],
                                                                                     worker_login=worker_login),
                                      reply_markup=AdminKeyboards.worker_statistics())

@router.callback_query(F.data == "add_workers")
async def usr_orders_list(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(page_list_workers=1)
    await state.set_state(AdminStates.add_workers)

    await callback.message.answer(
        text=texts.admin.usr_add_workers
    )
@router.message(AdminStates.add_workers)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)
    list_workers = tools.get_from_message_list_workers(message.text)
    mysql.multi_add('statistics', login=list_workers)
    status=mysql.multi_add('workers',login=list_workers)
    if status:
        await message.answer(
            text=texts.admin.add_workers_complete,
            reply_markup=AdminKeyboards.add_workers_complete()
        )
    else:
        await message.answer(
            text=texts.admin.add_workers_not_complete,
            reply_markup=AdminKeyboards.add_workers_not_complete()
        )




@router.callback_query(F.data == "delete_workers")
async def usr_orders_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.delete_workers)
    await state.update_data(page_list_workers=1)

    await callback.message.answer(
        text=texts.admin.usr_delete_workers
    )
@router.message(AdminStates.delete_workers)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    list_workers = tools.get_from_message_list_workers(message.text)
    mysql.multi_delete('statistics', login=list_workers)
    status=mysql.multi_delete('workers',login=list_workers)
    if status:
        await message.answer(
            text=texts.admin.delete_workers_complete,
            reply_markup=AdminKeyboards.delete_workers_complete()
        )
    else:
        await message.answer(
            text=texts.admin.delete_workers_not_complete,
            reply_markup=AdminKeyboards.delete_workers_not_complete()
        )






@router.callback_query(F.data.startswith('providers_page_'))
async def clb_list_message_next_last_page(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    user_data=await state.get_data()



    if tools.state_data_is_empty(user_data):
        user_data= tools.create_start_state_data()

    if callback.data == 'providers_page_start':
        user_data['page_list_providers'] = 1
    elif callback.data=='providers_page_next':
        user_data['page_list_providers']+=1
    elif callback.data=='providers_page_last':
        user_data['page_list_providers']-=1

    count = mysql.count_all('chats_providers')
    if count == 0:
        await callback.message.answer(
            text=texts.admin.usr_list_providers_empty,
            reply_markup=AdminKeyboards.page_list_providers_empty()
        )
        return

    max_page = count // 5 + (0 if count % 5 == 0 else 1)
    user_data['page_list_providers'] = tools.constrain(user_data['page_list_providers'],
                                                       min_=1,
                                                       max_=max_page)
    logging.debug(f'{user_data=} {max_page=}')
    list_message = mysql.search_n('chats_providers',
                                  step=user_data['page_list_providers'],
                                  count=5,
                                  sort_name='id')
    list_message=list(map(list,list_message))
    for i in range(len(list_message)):
        try:
            chat=await callback.bot.get_chat(list_message[i][1])
            list_message[i][0]=f'[{chat.title}]({chat.invite_link})'
        except:
            list_message[i][0]=''
    list_message_str = tools.get_string_list_message_providers(list_message)
    await state.update_data(page_list_providers=user_data['page_list_providers'])
    await callback.message.edit_text(
        text=texts.admin.usr_list_providers.format(list=list_message_str),
        reply_markup=AdminKeyboards.page_list_providers(page=user_data['page_list_providers'],
                                                      max_page=max_page,
                                                      count=count),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True)
    )

@router.callback_query(F.data == "add_providers")
async def usr_orders_list(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(page_list_providers=1)
    await state.set_state(AdminStates.add_providers)

    await callback.message.answer(
        text=texts.admin.usr_add_providers
    )
@router.message(AdminStates.add_providers)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)
    list_providers,list_add_providers = tools.get_from_message_list_providers(message.text)
    status=mysql.multi_add('chats_providers',chat_id=list_providers,add_chat_id=list_add_providers)
    if status:
        await message.answer(
            text=texts.admin.add_providers_complete,
            reply_markup=AdminKeyboards.add_providers_complete()
        )
    else:
        await message.answer(
            text=texts.admin.add_providers_not_complete,
            reply_markup=AdminKeyboards.add_providers_not_complete()
        )




@router.callback_query(F.data == "delete_providers")
async def usr_orders_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.delete_providers)
    await state.update_data(page_list_providers=1)

    await callback.message.answer(
        text=texts.admin.usr_delete_providers
    )
@router.message(AdminStates.delete_providers)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)

    list_providers = tools.get_from_message_list_providers_to_delete(message.text)
    status=mysql.multi_delete('chats_providers',chat_id=list_providers)
    if status:
        await message.answer(
            text=texts.admin.delete_providers_complete,
            reply_markup=AdminKeyboards.delete_providers_complete()
        )
    else:
        await message.answer(
            text=texts.admin.delete_providers_not_complete,
            reply_markup=AdminKeyboards.delete_providers_not_complete()
        )

@router.callback_query(F.data=='send_log')
async def upload_photo(callback: types.CallbackQuery):
    # Отправка файла из файловой системы
    try:
        log_from_pc = FSInputFile("core/logs/log.log")
    except:
        await callback.answer(
            'Невозможно открыть файл'
        )
        return
    if os.path.getsize("core/logs/log.log")==0:
        await callback.answer(
            text="Логи пустые"
        )
        return

    result = await callback.message.answer_document(
        log_from_pc,
        caption="Логи"
    )




# @router.message(Command('test'))
# async def cmd_test(message: types.Message,state:FSMContext):
#     user_data = await state.get_data()
#     await message.answer(str(user_data),
#                          parse_mode=None)
#     # apscheduler.print_jobs()
#     #logging.info(apscheduler.get_job(str(message.chat.id)))
#     #logging.info(mysql.check('users',str(message.chat.id)))
#     #await message.answer(str(sqlite.get_table('questions')))

# @router.message(Command('info'))
# async def cmd_info(message: types.Message,state:FSMContext,apscheduler:AsyncIOScheduler):
#     # user_data = await state.get_data()
#     # await message.answer(str(user_data))
#     # apscheduler.print_jobs()
#     await message.answer('info')
# @router.message(Command('help'))
# async def cmd_help(message: types.Message):
#     await message.answer('help')


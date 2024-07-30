from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    main = State()
    add_workers = State()
    delete_workers = State()
    add_providers = State()
    delete_providers = State()

class UserStates(StatesGroup):
    main = State()
    choice_type_message = State()
    write_message = State()
    get_photo=State()
    is_send_message=State()

    list_my_message=State()

from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    main = State()


class DashboardState(StatesGroup):
    main = State()
    statistics = State()
    users = State()
    broadcast = State()
    promocodes = State()
    banlist = State()
    maintenance = State()


class RemnashopState(StatesGroup):
    main = State()
    admins = State()
    referral = State()
    ads = State()
    plans = State()
    notifications = State()
    logs = State()


class RemnawaveState(StatesGroup):
    main = State()
    users = State()
    hosts = State()
    nodes = State()
    inbounds = State()

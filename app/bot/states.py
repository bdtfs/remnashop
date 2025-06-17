from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    main = State()


class Dashboard(StatesGroup):
    main = State()
    statistics = State()
    maintenance = State()


class DashboardBroadcast(StatesGroup):
    main = State()
    to_all = State()
    to_user = State()
    subscribed = State()
    unsubscribed = State()
    expired = State()
    last_sent = State()


class DashboardPromocodes(StatesGroup):
    main = State()
    list = State()
    create = State()
    delete = State()
    edit = State()


class DashboardUsers(StatesGroup):
    main = State()
    search = State()
    recent_registered = State()
    recent_activity = State()
    blacklist = State()
    unblock_all = State()

    user = State()
    statistics = State()
    role = State()
    subscription = State()
    transactions = State()


class DashboardRemnashop(StatesGroup):
    main = State()
    admins = State()
    referral = State()
    advertising = State()
    plans = State()
    notifications = State()
    logs = State()


class DashboardRemnawave(StatesGroup):
    main = State()
    users = State()
    hosts = State()
    nodes = State()
    inbounds = State()

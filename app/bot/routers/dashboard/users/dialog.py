from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    Row,
    ScrollingGroup,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from app.bot.states import Dashboard, DashboardUsers
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

from .getters import blacklist_getter, role_getter, user_getter
from .handlers import (
    on_block_toggle,
    on_role_selected,
    on_unblock_all,
    on_user_search,
    on_user_selected,
)

users = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-users"),
    Row(
        SwitchTo(
            I18nFormat("btn-users-search"),
            id="users.search",
            state=DashboardUsers.search,
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-users-recent-registered"),
            id="users.recent_registered",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-users-recent-activity"),
            id="users.recent_activity",
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-users-blacklist"),
            id="users.blacklist",
            state=DashboardUsers.blacklist,
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=Dashboard.main,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardUsers.main,
)

search = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-users-search"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard_users",
            state=DashboardUsers.main,
        ),
    ),
    MessageInput(func=on_user_search),
    IgnoreUpdate(),
    state=DashboardUsers.search,
)

unblock_all = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-users-unblock-all"),
    Row(
        Button(
            I18nFormat("btn-unblock-all-confirm"),
            id="blacklist.unblock_all_confirm",
            on_click=on_unblock_all,
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.blacklist",
            state=DashboardUsers.blacklist,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardUsers.unblock_all,
)

blacklist = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-users-blacklist"),
    ScrollingGroup(
        Select(
            text=Format("{item.telegram_id} ({item.name})"),
            id="blacklist.user",
            item_id_getter=lambda item: item.telegram_id,
            items="blocked_users",
            type_factory=int,
            on_click=on_user_selected,
        ),
        id="blacklist.scroll",
        width=1,
        height=7,
        hide_on_single_page=True,
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-blacklist-unblock-all"),
            id="blacklist.unblock_all",
            state=DashboardUsers.unblock_all,
            when=F["blocked_users_exists"],
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard_users",
            state=DashboardUsers.main,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardUsers.blacklist,
    getter=blacklist_getter,
)

user = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-users-user"),
    Row(
        Button(
            I18nFormat("btn-user-statistics"),
            id="user.statistics",
        ),
        Button(
            I18nFormat("btn-user-message"),
            id="user.message",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-user-subscription"),
            id="user.subscription",
        ),
        Button(
            I18nFormat("btn-user-transactions"),
            id="user.transactions",
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-user-change-role"),
            id="user.role",
            state=DashboardUsers.role,
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-user-block-toggle", is_blocked=Format("{is_blocked}")),
            id="user.block_toggle",
            on_click=on_block_toggle,
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-back-dashboard"),
            id="back.dashboard",
            state=Dashboard.main,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardUsers.user,
    getter=user_getter,
)

role = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-users-user-role"),
    Column(
        Select(
            text=I18nFormat("btn-user-role", role=Format("{item}")),
            id="select_role",
            item_id_getter=lambda item: item.value,
            items="roles",
            on_click=on_role_selected,
        )
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard_users",
            state=DashboardUsers.user,
        )
    ),
    IgnoreUpdate(),
    state=DashboardUsers.role,
    getter=role_getter,
)

router = Dialog(
    users,
    search,
    blacklist,
    unblock_all,
    user,
    role,
)

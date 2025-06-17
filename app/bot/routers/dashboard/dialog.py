from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo
from magic_filter import F

from app.bot.conditions import is_dev
from app.bot.states import (
    Dashboard,
    DashboardBroadcast,
    DashboardPromocodes,
    DashboardRemnashop,
    DashboardUsers,
    MainMenu,
)
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

from .remnawave.handlers import start_remnawave_window

dashboard = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard"),
    Row(
        SwitchTo(
            I18nFormat("btn-dashboard-statistics"),
            id="dashboard.statistics",
            state=Dashboard.statistics,
        ),
        Start(
            I18nFormat("btn-dashboard-users"),
            id="dashboard.users",
            state=DashboardUsers.main,
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-dashboard-broadcast"),
            id="dashboard.broadcast",
            state=DashboardBroadcast.main,
        ),
        Start(
            I18nFormat("btn-dashboard-promocodes"),
            id="dashboard.promocodes",
            state=DashboardPromocodes.main,
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-dashboard-maintenance"),
            id="dashboard.maintenance",
            state=Dashboard.maintenance,
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-dashboard-remnawave"),
            id="dashboard.remnawave",
            on_click=start_remnawave_window,
        ),
        Start(
            I18nFormat("btn-dashboard-remnashop"),
            id="dashboard.remnashop",
            state=DashboardRemnashop.main,
        ),
        when=is_dev,
    ),
    Row(
        Start(
            I18nFormat("btn-back-menu"),
            id="back.menu",
            state=MainMenu.main,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.main,
)

statistics = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-statistics"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=Dashboard.main,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.statistics,
)

maintenance = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-maintenance"),
    Row(
        Button(
            I18nFormat("btn-maintenance-global"),
            id="maintenance.global",
        ),
        Button(
            I18nFormat("btn-maintenance-purchase"),
            id="maintenance.purchase",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-maintenance-off"),
            id="maintenance.off",
        ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=Dashboard.main,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.maintenance,
)

router = Dialog(
    dashboard,
    statistics,
    maintenance,
)

import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo

from app.bot.states import Dashboard, DashboardRemnawave
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

from .getters import (
    hosts_getter,
    inbounds_getter,
    nodes_getter,
    system_getter,
    users_getter,
)

logger = logging.getLogger(__name__)


remnawave = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave"),
    Row(
        SwitchTo(
            I18nFormat("btn-remnawave-users"),
            id="remnawave.users",
            state=DashboardRemnawave.users,
        )
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-remnawave-hosts"),
            id="remnawave.hosts",
            state=DashboardRemnawave.hosts,
        ),
        SwitchTo(
            I18nFormat("btn-remnawave-nodes"),
            id="remnawave.nodes",
            state=DashboardRemnawave.nodes,
        ),
        SwitchTo(
            I18nFormat("btn-remnawave-inbounds"),
            id="remnawave.inbounds",
            state=DashboardRemnawave.inbounds,
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=Dashboard.main,
        )
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.main,
    getter=system_getter,
)

users = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-users"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=DashboardRemnawave.main,
        )
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.users,
    getter=users_getter,
)

hosts = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-hosts"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=DashboardRemnawave.main,
        )
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.hosts,
    getter=hosts_getter,
)

nodes = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-nodes"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=DashboardRemnawave.main,
        )
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.nodes,
    getter=nodes_getter,
)

inbounds = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-inbounds"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=DashboardRemnawave.main,
        )
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.inbounds,
    getter=inbounds_getter,
)


router = Dialog(
    remnawave,
    users,
    hosts,
    nodes,
    inbounds,
)

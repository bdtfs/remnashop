from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo

from app.bot.states import Dashboard, DashboardBroadcast
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

broadcast = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-broadcast"),
    Row(
        Button(
            I18nFormat("btn-broadcast-all"),
            id="broadcast.all",
        ),
        Button(
            I18nFormat("btn-broadcast-user"),
            id="broadcast.user",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-broadcast-subscribed"),
            id="broadcast.subscribed",
        ),
        Button(
            I18nFormat("btn-broadcast-unsubscribed"),
            id="broadcast.unsubscribed",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-broadcast-expired"),
            id="broadcast.expired",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-broadcast-last-message"),
            id="broadcast.last_message",
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
    state=DashboardBroadcast.main,
)


router = Dialog(broadcast)

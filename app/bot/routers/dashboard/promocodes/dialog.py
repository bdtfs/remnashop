from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo

from app.bot.states import Dashboard, DashboardPromocodes
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

promocodes = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-promocodes"),
    Row(
        Button(
            I18nFormat("btn-promocodes-list"),
            id="promocodes.list",
        ),
        Button(
            I18nFormat("btn-promocodes-search"),
            id="promocodes.search",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-promocodes-create"),
            id="promocodes.create",
        ),
        # Button(
        #     I18nFormat("btn-promocodes-delete"),
        #     id="promocodes.delete",
        # ),
        # Button(
        #     I18nFormat("btn-promocodes-edit"),
        #     id="promocodes.edit",
        # ),
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=Dashboard.main,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardPromocodes.main,
)

router = Dialog(promocodes)

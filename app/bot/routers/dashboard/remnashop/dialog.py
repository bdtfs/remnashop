from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo

from app.bot.states import DashboardState, RemnashopState
from app.bot.widgets import Audit, Banner, I18nFormat, IgnoreInput
from app.core.enums import BannerName

router = Dialog(
    Window(
        Banner(BannerName.DASHBOARD),
        I18nFormat("msg-remnashop"),
        Row(
            SwitchTo(
                I18nFormat("btn-remnashop-admins"),
                id="remnashop.admins",
                state=RemnashopState.admins,
            )
        ),
        Row(
            SwitchTo(
                I18nFormat("btn-remnashop-referral"),
                id="remnashop.referral",
                state=RemnashopState.referral,
            ),
            SwitchTo(
                I18nFormat("btn-remnashop-ads"),
                id="remnashop.ads",
                state=RemnashopState.ads,
            ),
        ),
        Row(
            SwitchTo(
                I18nFormat("btn-remnashop-plans"),
                id="remnashop.plans",
                state=RemnashopState.plans,
            ),
            SwitchTo(
                I18nFormat("btn-remnashop-notifications"),
                id="remnashop.notifications",
                state=RemnashopState.notifications,
            ),
        ),
        Row(
            Button(
                I18nFormat("btn-remnashop-logs"),
                id="remnashop.logs",
            ),
            Button(
                I18nFormat("btn-remnashop-audit"),
                id="remnashop.audit",
            ),
        ),
        Row(
            Start(
                I18nFormat("btn-back"),
                id="back.dashboard",
                state=DashboardState.main,
            )
        ),
        IgnoreInput(),
        state=RemnashopState.main,
    )
)

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Start

from app.bot.conditions import is_admin_or_dev
from app.bot.routers.dashboard.users.handlers import on_user_search
from app.bot.states import Dashboard, MainMenu
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

from .getters import menu_getter

menu = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-menu-profile"),
    I18nFormat("space"),
    I18nFormat("msg-menu-subscription"),
    # Row(
    #     Button(I18nFormat("btn-menu-connect"), id="menu.connect"),
    # ),
    # Row(
    #     Button(I18nFormat("btn-menu-trial"), id="menu.trial"),
    # ),
    Row(
        # Button(
        #     I18nFormat("btn-menu-promocode"),
        #     id="menu.promocode",
        # ),
        Button(
            I18nFormat("btn-menu-subscription"),
            id="menu.subscription",
        ),
    ),
    Row(
        Button(
            I18nFormat("btn-menu-invite"),
            id="menu.invite",
        ),
        Button(
            I18nFormat("btn-menu-support"),
            id="menu.support",
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-menu-dashboard"),
            id="menu.dashboard",
            state=Dashboard.main,
            when=is_admin_or_dev,
        ),
    ),
    MessageInput(func=on_user_search),
    IgnoreUpdate(),
    state=MainMenu.main,
    getter=menu_getter,
)

router = Dialog(menu)

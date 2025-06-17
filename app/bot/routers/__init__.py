from . import dashboard, menu
from .dashboard import broadcast, promocodes, remnashop, remnawave, users

routers = [
    menu.handlers.router,  # NOTE: Must be registered first to handle common entrypoints before dialogs
    menu.dialog.router,
    dashboard.dialog.router,
    users.dialog.router,
    broadcast.dialog.router,
    promocodes.dialog.router,
    remnashop.dialog.router,
    remnawave.dialog.router,
]

__all__ = [
    "routers",
]

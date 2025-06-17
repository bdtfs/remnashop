from aiogram_dialog import DialogManager

from app.bot.models.containers import AppContainer
from app.db.models import UserDto


async def admins_getter(dialog_manager: DialogManager, container: AppContainer, **kwargs) -> dict:
    devs: list[UserDto] = await container.services.user.get_devs()
    admins: list[UserDto] = await container.services.user.get_admins()

    return {"admins": devs + admins}

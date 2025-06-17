from aiogram_dialog import DialogManager

from app.db.models.dto import UserDto


async def menu_getter(dialog_manager: DialogManager, user: UserDto, **kwargs) -> dict:
    return {
        "id": str(user.telegram_id),
        "name": user.name,
        "status": None,
    }

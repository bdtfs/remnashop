from typing import Any, cast

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.core.config.app import AppConfig
from src.core.constants import USER_KEY
from src.core.enums import UserRole
from src.infrastructure.database.models.dto import UserDto
from src.services.user import UserService


@inject
async def user_getter(
    dialog_manager: DialogManager,
    config: AppConfig,
    user_service: FromDishka[UserService],
    **kwargs: Any,
) -> dict[str, Any]:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    start_data = cast(dict[str, Any], dialog_manager.start_data)

    target_telegram_id = start_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    return {
        "id": str(target_user.telegram_id),
        "username": target_user.username or False,
        "name": target_user.name,
        "role": target_user.role,
        "is_blocked": target_user.is_blocked,
        "status": None,
        "is_not_self": target_user.telegram_id != user.telegram_id,
        "can_edit": user.role > target_user.role or config.bot.dev_id == user.telegram_id,
    }


@inject
async def role_getter(
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    **kwargs: Any,
) -> dict[str, Any]:
    start_data = cast(dict[str, Any], dialog_manager.start_data)

    target_telegram_id = start_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    roles = [role for role in UserRole if role != target_user.role]
    return {"roles": roles}

from typing import Any, Union, cast

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, SubManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.bot.states import DashboardUser
from src.core.constants import USER_KEY
from src.core.enums import UserRole
from src.core.utils.formatters import format_user_log as log
from src.infrastructure.database.models.dto import UserDto
from src.infrastructure.taskiq.tasks.redirects import redirect_to_main_menu_task
from src.services.user import UserService


async def start_user_window(
    manager: Union[DialogManager, SubManager],
    target_telegram_id: int,
) -> None:
    await manager.start(
        state=DashboardUser.MAIN,
        data={"target_telegram_id": target_telegram_id},
        mode=StartMode.RESET_STACK,
    )


@inject
async def on_block_toggle(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
) -> None:
    start_data = cast(dict[str, Any], dialog_manager.start_data)
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = start_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"Attempted to toggle block for non-existent user '{target_telegram_id}'")

    blocked = not target_user.is_blocked

    await user_service.set_block(user=target_user, blocked=blocked)
    await redirect_to_main_menu_task.kiq(target_user)
    logger.info(
        f"{log(user)} Successfully {'blocked' if blocked else 'unblocked'} {log(target_user)}"
    )


@inject
async def on_role_select(
    callback: CallbackQuery,
    widget: Select[UserRole],
    dialog_manager: DialogManager,
    selected_role: UserRole,
    user_service: FromDishka[UserService],
) -> None:
    start_data = cast(dict[str, Any], dialog_manager.start_data)
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = start_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"Attempted to change role for non-existent user '{target_telegram_id}'")

    await user_service.set_role(user=target_user, role=selected_role)
    await redirect_to_main_menu_task.kiq(target_user)
    logger.info(
        f"{log(user)} Successfully changed role for {log(target_user)} to '{selected_role}'"
    )

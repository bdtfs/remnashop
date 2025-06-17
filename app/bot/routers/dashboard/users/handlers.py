import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.models import AppContainer
from app.bot.states import DashboardUsers
from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.enums import UserRole
from app.db.models.dto import UserDto

logger = logging.getLogger(__name__)


async def start_user_window(dialog_manager: DialogManager, target_user_id: int) -> None:
    await dialog_manager.start(state=DashboardUsers.user, data={"target_user_id": target_user_id})


async def on_user_search(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data.get(USER_KEY)

    if not (user.is_admin or user.is_dev):
        return

    if message.forward_from and not message.forward_from.is_bot:
        user_id = message.forward_from.id
    elif message.text and message.text.isdigit():
        user_id = int(message.text)
    else:
        return

    container: AppContainer = dialog_manager.middleware_data.get(APP_CONTAINER_KEY)
    target_user = await container.services.user.get(user_id)

    if target_user is None:
        # TODO: Notify not found user in db
        return

    logger.info(
        f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Searched for "
        f"[{target_user.role.upper()}:{target_user.telegram_id} ({target_user.name})]"
    )

    await start_user_window(dialog_manager, target_user.telegram_id)


async def on_user_selected(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    target_user_id: int,
) -> None:
    await start_user_window(dialog_manager, target_user_id)


async def on_role_selected(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    selected_role: str,
) -> None:
    user: UserDto = dialog_manager.middleware_data.get(USER_KEY)
    container: AppContainer = dialog_manager.middleware_data.get(APP_CONTAINER_KEY)
    target_user_id = dialog_manager.start_data.get("target_user_id")
    target_user = await container.services.user.get(telegram_id=target_user_id)

    if target_user.telegram_id == container.config.bot.dev_id:
        logger.warning(
            f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Trying to switch role for "
            f"[{target_user.role.upper()}:{target_user.telegram_id} ({target_user.name})]"
        )
        await start_user_window(dialog_manager, target_user_id)
        # TODO: BAN amogus?
        # TODO: Notify
        return

    logger.info(
        f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Switched role for "
        f"[{target_user.role.upper()}:{target_user.telegram_id} ({target_user.name})]"
    )
    await container.services.user.set_role(target_user, UserRole(selected_role))
    # TODO: Notify


async def on_block_toggle(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserDto = dialog_manager.middleware_data.get(USER_KEY)
    container: AppContainer = dialog_manager.middleware_data.get(APP_CONTAINER_KEY)
    target_user_id = dialog_manager.start_data.get("target_user_id")
    target_user = await container.services.user.get(telegram_id=target_user_id)

    if target_user.telegram_id == container.config.bot.dev_id:
        logger.warning(
            f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Tried to block "
            f"[{target_user.role.upper()}:{target_user.telegram_id} ({target_user.name})]"
        )
        await start_user_window(dialog_manager, target_user_id)
        # TODO: BAN amogus?
        # TODO: Notify
        return

    logger.info(
        f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Blocked "
        f"[{target_user.role.upper()}:{target_user.telegram_id} ({target_user.name})]"
    )
    await container.services.user.set_block(user=target_user, blocked=not target_user.is_blocked)
    # TODO: Notify


async def on_unblock_all(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserDto = dialog_manager.middleware_data.get(USER_KEY)
    container: AppContainer = dialog_manager.middleware_data.get(APP_CONTAINER_KEY)
    blocked_users = await container.services.user.get_blocked_users()

    for blocked_user in blocked_users:
        await container.services.user.set_block(user=blocked_user, blocked=False)

    logger.warning(f"[{user.role.upper()}:{user.telegram_id} ({user.name})] Unblocked all users")
    # TODO: Notify
    await dialog_manager.start(state=DashboardUsers.blacklist)

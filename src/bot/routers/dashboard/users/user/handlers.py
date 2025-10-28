from typing import Union
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger
from remnawave import RemnawaveSDK

from src.bot.states import DashboardUser
from src.core.constants import USER_KEY
from src.core.enums import SubscriptionStatus, UserRole
from src.core.utils.formatters import format_user_log as log
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.database.models.dto import UserDto
from src.infrastructure.taskiq.tasks.redirects import redirect_to_main_menu_task
from src.services.notification import NotificationService
from src.services.remnawave import RemnawaveService
from src.services.subscription import SubscriptionService
from src.services.transaction import TransactionService
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
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    blocked = not target_user.is_blocked
    await user_service.set_block(user=target_user, blocked=blocked)
    await redirect_to_main_menu_task.kiq(target_user)
    logger.info(f"{log(user)} {'Blocked' if blocked else 'Unblocked'} {log(target_user)}")


@inject
async def on_role_select(
    callback: CallbackQuery,
    widget: Select[UserRole],
    dialog_manager: DialogManager,
    selected_role: UserRole,
    user_service: FromDishka[UserService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    await user_service.set_role(user=target_user, role=selected_role)
    await redirect_to_main_menu_task.kiq(target_user)
    logger.info(f"{log(user)} Changed role to '{selected_role} for {log(target_user)}")


@inject
async def on_current_subscription(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    subscription_service: FromDishka[SubscriptionService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-subscription-empty"),
        )
        return

    await dialog_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_active_toggle(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    subscription_service: FromDishka[SubscriptionService],
    remnawave: FromDishka[RemnawaveSDK],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    new_status = (
        SubscriptionStatus.DISABLED if subscription.is_active else SubscriptionStatus.ACTIVE
    )

    remnawave_toggle_status = (
        remnawave.users.disable_user if subscription.is_active else remnawave.users.enable_user
    )

    await remnawave_toggle_status(uuid=str(subscription.user_remna_id))
    subscription.status = new_status
    await subscription_service.update(subscription)
    logger.info(
        f"{log(user)} Toggled subscription status to '{new_status}' for '{target_telegram_id}'"
    )


@inject
async def on_subscription_delete(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    subscription.status = SubscriptionStatus.DELETED
    await subscription_service.update(subscription)
    await user_service.delete_current_subscription(target_telegram_id)
    await remnawave_service.delete_user(target_user)
    logger.info(f"{log(user)} Deleted subscription for user '{target_telegram_id}'")
    await dialog_manager.switch_to(state=DashboardUser.MAIN)


@inject
async def on_devices(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    remnawave_service: FromDishka[RemnawaveService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    devices = await remnawave_service.get_devices_user(target_user)

    if not devices:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-devices-empty"),
        )
        return

    await dialog_manager.switch_to(state=DashboardUser.DEVICES_LIST)


@inject
async def on_device_delete(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    user_service: FromDishka[UserService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    await sub_manager.load_data()
    selected_device = sub_manager.item_id

    user: UserDto = sub_manager.middleware_data[USER_KEY]
    target_telegram_id = sub_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    devices = await remnawave_service.delete_device(user=target_user, hwid=selected_device)
    logger.info(f"{log(user)} Deleted device '{selected_device}' for user '{target_telegram_id}'")

    if devices:
        return

    await sub_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_reset_traffic(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    subscription_service: FromDishka[SubscriptionService],
    remnawave: FromDishka[RemnawaveSDK],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    await remnawave.users.reset_user_traffic(uuid=str(subscription.user_remna_id))
    logger.info(f"{log(user)} Reset trafic for user '{target_telegram_id}'")


@inject
async def on_discount_select(
    callback: CallbackQuery,
    widget: Select[int],
    dialog_manager: DialogManager,
    selected_discount: int,
    user_service: FromDishka[UserService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.info(f"{log(user)} Selected discount '{selected_discount}'")
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    target_user.personal_discount = selected_discount
    await user_service.update(user=target_user)
    logger.info(f"{log(user)} Changed discount to '{selected_discount}' for '{target_telegram_id}'")
    await dialog_manager.switch_to(state=DashboardUser.MAIN)


@inject
async def on_discount_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    if message.text is None or not (message.text.isdigit() and 0 <= int(message.text) <= 100):
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-invalid-number"),
        )
        return

    number = int(message.text)
    target_user.personal_discount = number
    await user_service.update(user=target_user)
    logger.info(f"{log(user)} Changed discount to '{number}' for '{target_telegram_id}'")
    await dialog_manager.switch_to(state=DashboardUser.MAIN)


@inject
async def on_traffic_limit_select(
    callback: CallbackQuery,
    widget: Select[int],
    dialog_manager: DialogManager,
    selected_traffic: int,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.info(f"{log(user)} Selected traffic '{selected_traffic}'")
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    subscription.traffic_limit = selected_traffic
    await subscription_service.update(subscription)

    await remnawave_service.updated_user(
        user=target_user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
        not_update_expire_at=True,
        reset_traffic=False,
    )

    logger.info(
        f"{log(user)} Changed traffic limit to '{selected_traffic}' for '{target_telegram_id}'"
    )
    await dialog_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_traffic_limit_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    notification_service: FromDishka[NotificationService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    if message.text is None or not (message.text.isdigit() and int(message.text) > 0):
        logger.warning(f"{log(user)} Invalid traffic limit input: '{message.text}'")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-invalid-number"),
        )
        return

    number = int(message.text)
    subscription.traffic_limit = number
    await subscription_service.update(subscription)

    await remnawave_service.updated_user(
        user=target_user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
        not_update_expire_at=True,
        reset_traffic=False,
    )

    logger.info(f"{log(user)} Changed traffic limit to '{number}' for '{target_telegram_id}'")
    await dialog_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_device_limit_select(
    callback: CallbackQuery,
    widget: Select[int],
    dialog_manager: DialogManager,
    selected_device: int,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.info(f"{log(user)} Selected device limit '{selected_device}'")
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    subscription.device_limit = selected_device
    await subscription_service.update(subscription)

    await remnawave_service.updated_user(
        user=target_user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
        not_update_expire_at=True,
        reset_traffic=False,
    )

    logger.info(
        f"{log(user)} Changed device limit to '{selected_device}' for '{target_telegram_id}'"
    )
    await dialog_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_device_limit_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    notification_service: FromDishka[NotificationService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    if message.text is None or not (message.text.isdigit() and int(message.text) > 0):
        logger.warning(f"{log(user)} Invalid device limit input: '{message.text}'")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-invalid-number"),
        )
        return

    number = int(message.text)
    subscription.device_limit = number
    await subscription_service.update(subscription)

    await remnawave_service.updated_user(
        user=target_user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
        not_update_expire_at=True,
        reset_traffic=False,
    )

    logger.info(f"{log(user)} Changed device limit to '{number}' for '{target_telegram_id}'")
    await dialog_manager.switch_to(state=DashboardUser.SUBSCRIPTION)


@inject
async def on_squad_select(
    callback: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    selected_squad: UUID,
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    remnawave_service: FromDishka[RemnawaveService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    target_user = await user_service.get(telegram_id=target_telegram_id)

    if not target_user:
        raise ValueError(f"User '{target_telegram_id}' not found")

    subscription = await subscription_service.get_current(target_telegram_id)

    if not subscription:
        raise ValueError(f"Current subscription for user '{target_telegram_id}' not found")

    if selected_squad in subscription.internal_squads:
        updated_internal_squads = [s for s in subscription.internal_squads if s != selected_squad]
        logger.info(f"{log(user)} Unset squad '{selected_squad}'")
    else:
        updated_internal_squads = [*subscription.internal_squads, selected_squad]
        logger.info(f"{log(user)} Set squad '{selected_squad}'")

    subscription.internal_squads = updated_internal_squads
    await subscription_service.update(subscription)
    await remnawave_service.updated_user(
        user=target_user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
        not_update_expire_at=True,
        reset_traffic=False,
    )


@inject
async def on_transactions(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    transaction_service: FromDishka[TransactionService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    target_telegram_id = dialog_manager.dialog_data["target_telegram_id"]
    transactions = await transaction_service.get_by_user(target_telegram_id)

    if not transactions:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-user-transactions-empty"),
        )
        return

    await dialog_manager.switch_to(state=DashboardUser.TRANSACTIONS_LIST)


async def on_transaction_select(
    callback: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    selected_transaction: UUID,
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.info(f"{log(user)} Selected transaction '{selected_transaction}'")
    dialog_manager.dialog_data["selected_transaction"] = selected_transaction
    await dialog_manager.switch_to(state=DashboardUser.TRANSACTION)

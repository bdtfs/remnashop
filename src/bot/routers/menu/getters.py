from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.core.utils.formatters import (
    i18n_format_device_limit,
    i18n_format_expire_time,
    i18n_format_traffic_limit,
)
from src.infrastructure.database.models.dto import UserDto
from src.services.plan import PlanService
from src.services.subscription import SubscriptionService


@inject
async def menu_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    plan_service: FromDishka[PlanService],
    subscription_service: FromDishka[SubscriptionService],
    **kwargs: Any,
) -> dict[str, Any]:
    plan = await plan_service.get_trial_plan()
    has_used_trial = await subscription_service.has_used_trial(user)

    if not user.current_subscription:
        return {
            "user_id": str(user.telegram_id),
            "user_name": user.name,
            "status": None,
            "is_privileged": user.is_privileged,
            "trial_available": not user.current_subscription and not has_used_trial and plan,
            "is_trial": False,
            "personal_discount": user.personal_discount,
        }

    return {
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "status": user.current_subscription.status,
        "type": user.current_subscription.get_subscription_type,
        "traffic_limit": i18n_format_traffic_limit(user.current_subscription.traffic_limit),
        "device_limit": i18n_format_device_limit(user.current_subscription.device_limit),
        "expire_time": i18n_format_expire_time(user.current_subscription.expire_at),
        "is_privileged": user.is_privileged,
        "is_trial": user.current_subscription.is_trial,
        "personal_discount": user.personal_discount,
    }

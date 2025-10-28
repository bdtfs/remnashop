import traceback
from typing import Any, Awaitable, Callable, Optional, cast

from aiogram.types import ErrorEvent, TelegramObject
from aiogram.types import User as AiogramUser
from aiogram.utils.formatting import Text

from src.core.enums import MiddlewareEventType
from src.infrastructure.taskiq.tasks.notifications import send_error_notification_task

from .base import EventTypedMiddleware


class ErrorMiddleware(EventTypedMiddleware):
    __event_types__ = [MiddlewareEventType.ERROR]

    async def middleware_logic(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        aiogram_user: Optional[AiogramUser] = self._get_aiogram_user(event)

        if aiogram_user:
            user_id = str(aiogram_user.id)
            user_name = aiogram_user.full_name
            username = aiogram_user.username
        else:
            user_id = None

        error_event = cast(ErrorEvent, event)
        traceback_str = traceback.format_exc()
        error_type_name = type(error_event.exception).__name__
        error_message = Text(str(error_event.exception)[:512])

        await send_error_notification_task.kiq(
            error_id=user_id or error_event.update.update_id,
            traceback_str=traceback_str,
            i18n_kwargs={
                "user": bool(user_id),
                "user_id": str(user_id),
                "user_name": user_name,
                "username": username or False,
                "error": f"{error_type_name}: {error_message.as_html()}",
            },
        )

        return await handler(event, data)

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.types import User as AiogramUser

from app.core.enums import UserRole
from app.db import SQLSessionContext
from app.db.models.dto import UserDto
from app.db.models.sql import User

from .base import CrudService

if TYPE_CHECKING:
    from app.bot.middlewares import I18nMiddleware

logger = logging.getLogger(__name__)


class UserService(CrudService):
    async def create(
        self,
        aiogram_user: AiogramUser,
        i18n: I18nMiddleware,
        is_dev: bool = False,  # TODO: config in CrudService
    ) -> UserDto:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            db_user = User(
                telegram_id=aiogram_user.id,
                name=aiogram_user.full_name,
                language=(
                    aiogram_user.language_code
                    if aiogram_user.language_code in i18n.locales
                    else i18n.default_locale
                ),
                role=UserRole.DEV if is_dev else UserRole.USER,
            )
            await uow.commit(db_user)
        logger.info(f"[User:{db_user.telegram_id} ({db_user.name})] Created in database")
        return db_user.dto()

    async def _get(
        self,
        getter: Callable[[Any], Awaitable[Optional[User]]],
        key: Any,
    ) -> Optional[User]:
        return await getter(key)

    async def get(self, telegram_id: int) -> Optional[UserDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            db_user = await repository.users.get(telegram_id=telegram_id)
            return db_user.dto() if db_user else None

    async def update(self, user: UserDto, **data: Any) -> Optional[UserDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            for key, value in data.items():
                setattr(user, key, value)
            db_user = await repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
            return db_user.dto() if db_user else None

    async def count(self) -> int:
        async with SQLSessionContext(session_pool=self.session_pool) as (repository, uow):
            return await repository.users.count()

    async def get_devs(self) -> list[UserDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            devs = await repository.users.filter_by_role(UserRole.DEV)
            return [dev.dto() for dev in devs]

    async def get_admins(self) -> list[UserDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            admins = await repository.users.filter_by_role(UserRole.ADMIN)
            return [admin.dto() for admin in admins]

    async def get_blocked_users(self) -> list[UserDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            users = await repository.users.filter_by_blocked()
            return [user.dto() for user in users]

    async def set_block(self, user: UserDto, blocked: bool) -> None:
        user.is_blocked = blocked
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            await repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        logger.info(f"[User:{user.telegram_id} ({user.name})] Set is_blocked -> '{blocked}'")

    async def set_bot_blocked(self, user: UserDto, blocked: bool) -> None:
        user.is_bot_blocked = blocked
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            await repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        logger.info(f"[User:{user.telegram_id} ({user.name})] Set is_bot_blocked -> '{blocked}'")

    async def set_role(self, user: UserDto, role: UserRole) -> None:
        user.role = role
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            await repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        logger.info(f"[User:{user.telegram_id} ({user.name})] Set role -> '{role}'")

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from app.bot.filters import IsPrivate
from app.bot.middlewares import (
    ErrorMiddleware,
    GarbageMiddleware,
    I18nMiddleware,
    ThrottlingMiddleware,
    UserMiddleware,
)
from app.bot.routers import routers

from .i18n import create_i18n_middleware
from .redis import create_redis
from .remnawave import create_remnawave
from .session_pool import create_session_pool

if TYPE_CHECKING:
    from app.core.config import AppConfig

logger = logging.getLogger(__name__)


def create_dispatcher(config: AppConfig) -> Dispatcher:
    key_builder = DefaultKeyBuilder(with_destiny=True)
    redis: Redis = create_redis(url=config.redis.dsn())

    error_middleware = ErrorMiddleware()
    user_middleware = UserMiddleware()
    i18n_middleware: I18nMiddleware = create_i18n_middleware(config)
    garbage_middleware = GarbageMiddleware()
    throttling_middleware = ThrottlingMiddleware()

    dispatcher = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            key_builder=key_builder,
        ),
        config=config,
        session_pool=create_session_pool(config=config),
        # redis= # TODO: redis repository for cache
        i18n_middleware=i18n_middleware,
        remnawave=create_remnawave(config=config),
    )

    # request -> outer -> filter -> inner -> handler #
    dispatcher.update.filter(IsPrivate())

    error_middleware.setup_outer(dispatcher)
    user_middleware.setup_outer(dispatcher)
    i18n_middleware.setup_inner(dispatcher)
    garbage_middleware.setup_inner(dispatcher)
    throttling_middleware.setup_outer(dispatcher)

    dispatcher.include_routers(*routers)
    setup_dialogs(dispatcher)
    return dispatcher

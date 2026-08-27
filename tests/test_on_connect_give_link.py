"""Tests for on_connect_give_link handler -- 'just give me the link' submenu action."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from src.bot.routers.menu.handlers import on_connect_give_link
from src.core.constants import USER_KEY
from tests.conftest import make_dialog_manager, make_subscription, make_user, unwrap_inject

_UNSET = object()


def _setup(*, subscription=_UNSET):
    user = make_user(
        telegram_id=450987966,
        name="Анастасия",
        subscription=make_subscription() if subscription is _UNSET else subscription,
    )

    notification_service = AsyncMock()

    dm = make_dialog_manager()
    dm.middleware_data[USER_KEY] = user

    callback = MagicMock()
    widget = MagicMock()

    return callback, widget, dm, notification_service, user


class TestOnConnectGiveLink:

    async def test_sends_subscription_link_as_code_message(self):
        callback, widget, dm, ntf, user = _setup()
        raw_fn = unwrap_inject(on_connect_give_link)

        await raw_fn(callback, widget, dm, ntf)

        ntf.notify_user.assert_called_once()
        payload = ntf.notify_user.call_args[1]["payload"]
        assert payload.i18n_key == "msg-menu-connect-link"
        assert payload.i18n_kwargs == {"url": user.current_subscription.url}

    async def test_no_subscription_sends_nothing(self):
        callback, widget, dm, ntf, _user = _setup(subscription=None)
        raw_fn = unwrap_inject(on_connect_give_link)

        await raw_fn(callback, widget, dm, ntf)

        ntf.notify_user.assert_not_called()

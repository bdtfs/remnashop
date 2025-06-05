import logging
from typing import Any, Callable, Optional

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo
from remnawave_api import RemnawaveSDK
from remnawave_api.models import (
    HostsResponseDto,
    InboundsResponseDto,
    NodesResponseDto,
    StatisticResponseDto,
)

from app.bot.states import DashboardState, RemnawaveState
from app.bot.widgets import Banner, I18nFormat, IgnoreInput
from app.core.constants import REMNAWAVE_KEY
from app.core.enums import BannerName
from app.core.formatters import (
    format_bytes,
    format_country_code,
    format_duration,
    format_percent,
)

logger = logging.getLogger(__name__)


async def on_click(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    remnawave: RemnawaveSDK = dialog_manager.middleware_data.get(REMNAWAVE_KEY)

    try:
        status = await remnawave.system.get_stats()
    except Exception as exception:
        logger.error(f"Remnawave: {exception}")
        await callback.message.answer(
            "Failed to connect to Remnawave. Please check your configuration.",
        )  # TODO: service notification
        return

    await dialog_manager.start(
        RemnawaveState.main,
    )


async def system_getter(
    dialog_manager: DialogManager,
    remnawave: RemnawaveSDK,
    i18n_format: Callable[[str, Optional[dict[str, Any]]], str],
    **kwargs,
) -> dict:
    stats: StatisticResponseDto = await remnawave.system.get_stats()
    return {
        "cpu_cores": stats.cpu.physical_cores,
        "cpu_threads": stats.cpu.cores,
        "ram_used": format_bytes(stats.memory.active, i18n_format),
        "ram_total": format_bytes(stats.memory.total, i18n_format),
        "ram_used_percent": format_percent(stats.memory.active, stats.memory.total),
        "uptime": format_duration(stats.uptime, i18n_format, True),
    }


async def users_getter(dialog_manager: DialogManager, remnawave: RemnawaveSDK, **kwargs) -> dict:
    stats: StatisticResponseDto = await remnawave.system.get_stats()
    return {
        "users_total": str(stats.users.total_users),
        "users_active": str(stats.users.status_counts.active),
        "users_disabled": str(stats.users.status_counts.disabled),
        "users_limited": str(stats.users.status_counts.limited),
        "users_expired": str(stats.users.status_counts.expired),
        "online_last_day": str(stats.online_stats.last_day),
        "online_last_week": str(stats.online_stats.last_week),
        "online_never": str(stats.online_stats.never_online),
        "online_now": str(stats.online_stats.online_now),
    }


async def hosts_getter(
    dialog_manager: DialogManager,
    remnawave: RemnawaveSDK,
    i18n_format: Callable[[str, Optional[dict[str, Any]]], str],
    **kwargs,
) -> dict:
    hosts: HostsResponseDto = await remnawave.hosts.get_all_hosts()

    hosts_text = "\n".join(
        i18n_format(
            "msg-remnawave-host-details",
            {
                "remark": host.remark,
                "status": "off" if host.is_disabled else "on",
                "address": host.address,
                "port": str(host.port),
                "inbound_uuid": str(host.inbound_uuid),
            },
        )
        for host in hosts.response
    )

    return {"hosts": hosts_text}


async def nodes_getter(
    dialog_manager: DialogManager,
    remnawave: RemnawaveSDK,
    i18n_format: Callable[[str, Optional[dict[str, Any]]], str],
    **kwargs,
) -> dict:
    nodes: NodesResponseDto = await remnawave.nodes.get_all_nodes()

    nodes_text = "\n".join(
        i18n_format(
            "msg-remnawave-node-details",
            {
                "country": format_country_code(node.country_code),
                "name": node.name,
                "status": "on" if node.is_connected else "off",
                "address": node.address,
                "port": str(node.port),
                "xray_uptime": format_duration(str(node.xray_uptime), i18n_format, True),
                "users_online": node.users_online,
                "traffic_used": format_bytes(node.traffic_used_bytes, i18n_format),
                "traffic_limit": (
                    format_bytes(node.traffic_limit_bytes, i18n_format, True)
                    if node.traffic_limit_bytes > 0
                    else "∞"
                ),
            },
        )
        for node in nodes.response
    )

    return {"nodes": nodes_text}


async def inbounds_getter(
    dialog_manager: DialogManager,
    remnawave: RemnawaveSDK,
    i18n_format: Callable[[str, Optional[dict[str, Any]]], str],
    **kwargs,
) -> dict:
    inbounds: InboundsResponseDto = await remnawave.inbounds.get_inbounds()

    inbounds_text = "\n".join(
        i18n_format(
            "msg-remnawave-inbound-details",
            {
                "uuid": str(inbound.uuid),
                "tag": inbound.tag,
                "type": inbound.type,
                "port": inbound.port,
                "network": inbound.network,
                "security": inbound.security,
            },
        )
        for inbound in inbounds.response
    )

    return {"inbounds": inbounds_text}


remnawave = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave"),
    Row(
        SwitchTo(
            I18nFormat("btn-remnawave-users"),
            id="remnawave.users",
            state=RemnawaveState.users,
        )
    ),
    Row(
        SwitchTo(
            I18nFormat("btn-remnawave-hosts"),
            id="remnawave.hosts",
            state=RemnawaveState.hosts,
        ),
        SwitchTo(
            I18nFormat("btn-remnawave-nodes"),
            id="remnawave.nodes",
            state=RemnawaveState.nodes,
        ),
        SwitchTo(
            I18nFormat("btn-remnawave-inbounds"),
            id="remnawave.inbounds",
            state=RemnawaveState.inbounds,
        ),
    ),
    Row(
        Start(
            I18nFormat("btn-back"),
            id="back.dashboard",
            state=DashboardState.main,
        )
    ),
    IgnoreInput(),
    state=RemnawaveState.main,
    getter=system_getter,
)

users = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-users"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=RemnawaveState.main,
        )
    ),
    IgnoreInput(),
    state=RemnawaveState.users,
    getter=users_getter,
)

hosts = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-hosts"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=RemnawaveState.main,
        )
    ),
    IgnoreInput(),
    state=RemnawaveState.hosts,
    getter=hosts_getter,
)

nodes = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-nodes"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=RemnawaveState.main,
        )
    ),
    IgnoreInput(),
    state=RemnawaveState.nodes,
    getter=nodes_getter,
)

inbounds = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-remnawave-inbounds"),
    Row(
        SwitchTo(
            I18nFormat("btn-back"),
            id="back.remnawave",
            state=RemnawaveState.main,
        )
    ),
    IgnoreInput(),
    state=RemnawaveState.inbounds,
    getter=inbounds_getter,
)


router = Dialog(
    remnawave,
    users,
    hosts,
    nodes,
    inbounds,
)

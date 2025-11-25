from typing import Optional, Union

from pydantic import Field, SecretStr

from src.core.enums import (
    AccessMode,
    Currency,
    ReferralAccrualStrategy,
    ReferralLevel,
    ReferralRewardStrategy,
    ReferralRewardType,
    SystemNotificationType,
    UserNotificationType,
)

from .base import BaseDto, TrackableDto


class SystemNotificationDto(TrackableDto):  # == SystemNotificationType
    bot_lifetime: bool = True
    bot_update: bool = True
    user_registered: bool = True
    subscription: bool = True
    promocode_activated: bool = True
    trial_getted: bool = True
    node_status: bool = True
    user_first_connected: bool = True
    user_hwid: bool = True
    # TODO: Add torrent_block
    # TODO: Add traffic_overuse

    def is_enabled(self, ntf_type: SystemNotificationType) -> bool:
        return getattr(self, ntf_type.value.lower(), False)


class UserNotificationDto(TrackableDto):  # == UserNotificationType
    expires_in_3_days: bool = True
    expires_in_2_days: bool = True
    expires_in_1_days: bool = True
    expired: bool = True
    limited: bool = True

    def is_enabled(self, ntf_type: UserNotificationType) -> bool:
        return getattr(self, ntf_type.value.lower(), False)


class ReferralRewardSettingsDto(BaseDto):
    type: ReferralRewardType = ReferralRewardType.EXTRA_DAYS
    strategy: ReferralRewardStrategy = ReferralRewardStrategy.AMOUNT
    config: dict[ReferralLevel, int] = {ReferralLevel.FIRST: 5}


class ReferralSettingsDto(TrackableDto):
    enable: bool = True
    level: ReferralLevel = ReferralLevel.FIRST
    accrual_strategy: ReferralAccrualStrategy = ReferralAccrualStrategy.ON_FIRST_PAYMENT
    reward: ReferralRewardSettingsDto = ReferralRewardSettingsDto()


class SettingsDto(TrackableDto):
    id: Optional[int] = Field(default=None, frozen=True)

    rules_required: bool = False
    channel_required: bool = False

    rules_link: SecretStr = SecretStr("https://telegram.org/tos/")
    channel_id: Optional[int] = False
    channel_link: SecretStr = SecretStr("@remna_shop")

    access_mode: AccessMode = AccessMode.PUBLIC
    default_currency: Currency = Currency.XTR

    user_notifications: UserNotificationDto = UserNotificationDto()
    system_notifications: SystemNotificationDto = SystemNotificationDto()

    referral: ReferralSettingsDto = ReferralSettingsDto()

    @property
    def channel_has_username(self) -> bool:
        return self.channel_link.get_secret_value().startswith("@")

    @property
    def get_url_channel_link(self) -> str:
        if self.channel_has_username:
            return f"t.me/{self.channel_link.get_secret_value()[1:]}"
        else:
            return self.channel_link.get_secret_value()

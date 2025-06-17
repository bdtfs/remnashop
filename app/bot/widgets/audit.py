from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager, DialogProtocol
from aiogram_dialog.widgets.kbd import Button, Keyboard


class Audit(Keyboard):
    def __init__(self, button: Button) -> None:
        super().__init__()
        self.button = button

    async def _render_keyboard(self, data: dict, dialog_manager: DialogManager) -> str:
        return await self.button._render_keyboard(data, dialog_manager)

    async def process_callback(
        self,
        callback: CallbackQuery,
        dialog_protocol: DialogProtocol,
        dialog_manager: DialogManager,
    ) -> bool:
        # TODO: implement audit logging
        # container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]
        return await self.button.process_callback(callback, dialog_protocol, dialog_manager)

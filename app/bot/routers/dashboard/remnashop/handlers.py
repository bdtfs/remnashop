from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select


async def on_role_removed(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    selected_user: str,
):
    await callback.answer(f"Удалить админа: {selected_user}")

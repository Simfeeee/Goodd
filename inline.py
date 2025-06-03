
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def approval_keyboard(post_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve:{post_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{post_id}")]
    ])

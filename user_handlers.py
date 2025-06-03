
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.inline import approval_keyboard
from app.sources.realnoevremya import fetch_realnoevremya
from app.utils.storage import is_duplicate, mark_as_published

router = Router()
admin_user_id = int(os.getenv("ADMIN_ID"))

@router.message(Command("update"))
async def cmd_update(message: Message):
    await message.answer("🔄 Готовлю новость...")

    news_items = fetch_realnoevremya()
    for item in news_items:
        if is_duplicate(item["id"]):
            continue

        post_text = f"<b>{item['title']}</b>

{item['summary']}

Источник: {item['source']}"
        await message.bot.send_message(chat_id=admin_user_id, text=post_text, reply_markup=approval_keyboard(item["id"]))
        break

@router.callback_query(F.data.startswith("approve:"))
async def callback_approve(call: CallbackQuery):
    post_id = call.data.split(":")[1]
    mark_as_published(post_id)
    await call.message.edit_reply_markup()
    await call.message.answer("✅ Новость опубликована")

@router.callback_query(F.data.startswith("reject:"))
async def callback_reject(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("❌ Новость отклонена")

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from parser import get_latest_news
from translator import translate_to_russian
from summarizer import summarize_and_analyze, get_emotional_reaction
from emoji_utils import get_topic_emojis
from datetime import datetime
from news_log import load_sent_links, save_sent_links

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
admin_user_id = 1818993268

PENDING_POSTS = {}

def get_reaction_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Нравится", callback_data="like"),
            InlineKeyboardButton(text="🤔 Интересно", callback_data="think"),
            InlineKeyboardButton(text="👎 Не согласен", callback_data="disagree"),
        ]
    ])

def get_approval_keyboard(post_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve:{post_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{post_id}")
        ]
    ])

async def send_latest_news():
    news = get_latest_news()
    sent_links = load_sent_links()
    for item in news:
        if item["link"] in sent_links:
            continue
        translated_summary = translate_to_russian(item["summary"])
        analysis = summarize_and_analyze(item["summary"])
        emotion = get_emotional_reaction(item["summary"])
        emojis = get_topic_emojis(item["title"] + " " + translated_summary)
        message = (
            f"🗞 <b>{item['title']} {emojis}</b>\n\n"
            f"🌍 {translated_summary}\n\n"
            f"🧠 <i>{analysis}</i>\n\n"
            f"{emotion}"
        )
        post_id = str(hash(item["link"]))
        PENDING_POSTS[post_id] = {
            "message": message,
            "link": item["link"],
            "title": item["title"]
        }
        await bot.send_message(chat_id=admin_user_id, text=f"📝 <b>Предпросмотр поста:</b>\n\n{message}", reply_markup=get_approval_keyboard(post_id))
        break

@dp.callback_query(F.data.startswith("approve:"))
async def approve_post(callback: CallbackQuery):
    post_id = callback.data.split(":")[1]
    post = PENDING_POSTS.pop(post_id, None)
    if post:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=post["message"], reply_markup=get_reaction_keyboard())
        await bot.send_message(chat_id=admin_user_id, text=f"✅ Новость опубликована: '{post['title']}'")
        sent_links = load_sent_links()
        sent_links.add(post["link"])
        save_sent_links(sent_links)
    await callback.answer("Публикация отправлена.")

@dp.callback_query(F.data.startswith("reject:"))
async def reject_post(callback: CallbackQuery):
    post_id = callback.data.split(":")[1]
    post = PENDING_POSTS.pop(post_id, None)
    if post:
        await bot.send_message(chat_id=admin_user_id, text=f"🚫 Публикация отклонена: '{post['title']}'")
    await callback.answer("Отклонено.")

@dp.message(Command("обновить"))
async def cmd_update(message: types.Message):
    await message.answer("🔄 Готовлю новость...")
    await send_latest_news()
    await message.answer("📩 Новость отправлена на модерацию.")

from scheduler import start_scheduler
async def main():
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
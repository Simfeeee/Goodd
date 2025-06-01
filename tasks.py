from config import TELEGRAM_CHANNEL_ID
from parser import get_latest_news
from translator import translate_to_russian
from summarizer import summarize_and_analyze, get_emotional_reaction
from emoji_utils import get_topic_emojis
from news_log import load_sent_links, save_sent_links
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

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

async def send_latest_news(bot: Bot):
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
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, reply_markup=get_reaction_keyboard())
        await bot.send_message(chat_id=admin_user_id, text=f"✅ Новость опубликована: '{item['title']}'")
        sent_links.add(item['link'])
        save_sent_links(sent_links)
        break

async def send_evening_digest(bot: Bot):
    news = get_latest_news()
    sent_links = load_sent_links()
    digest = "📰 <b>Вечерняя политическая сводка</b>\n\n"
    count = 0
    for item in news:
        if item["link"] in sent_links:
            continue
        translated_summary = translate_to_russian(item["summary"])
        analysis = summarize_and_analyze(item["summary"])
        emotion = get_emotional_reaction(item["summary"])
        emojis = get_topic_emojis(item["title"] + " " + translated_summary)
        digest += (
            f"{count+1}️⃣ <b>{item['title']} {emojis}</b>\n"
            f"🌍 {translated_summary}\n"
            f"🧠 <i>{analysis}</i>\n"
            f"{emotion}\n\n"
        )
        sent_links.add(item["link"])
        count += 1
        if count >= 5:
            break
    if count > 0:
        digest += "📅 Время публикации: 21:00"
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=digest)
        await bot.send_message(chat_id=admin_user_id, text="📩 Вечерняя сводка опубликована.")
        save_sent_links(sent_links)
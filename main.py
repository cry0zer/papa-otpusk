import telebot
from telebot import types
import requests
from flask import Flask
from threading import Thread

# --- ФЕЙКОВЫЙ СЕРВЕР ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Запускаем веб-сервер на порту 8080 для Render
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------

TOKEN = "8730274244:AAFS2Ehm_knkwivPhPRI9lmEmt1M1S52erw"
bot = telebot.TeleBot(TOKEN)

# Настройка ответов
AUTO_REPLY_HTML = (
    "👋 <b>Я В ОТПУСКЕ И ТЕЛЕФОН НЕ БЕРУ.</b>\n\n"
    "По всем вопросам пишите тем, кто работает:\n"
    "• <b>Техника / разработка:</b> @ivan_dev\n"
    "• <b>Документы / оплаты:</b> @olga_paper\n"
    "• <b>Срочно / завал:</b> @support_team\n\n"
    "Вернусь — прочту (может быть). Удачи!"
)

# Функция для получения URL случайного мема
def get_random_meme_url():
    try:
        r = requests.get("https://meme-api.com/gimme", timeout=5)
        r.raise_for_status()
        data = r.json()
        
        # Если пришел nsfw (неприличный) мем, пробуем еще раз
        if data.get("nsfw"):
             return get_random_meme_url()
             
        return data.get("url")
    except Exception:
        return None

# Хэндлер на любые сообщения
@bot.message_handler(content_types=['text', 'photo', 'sticker', 'voice', 'document'])
def reply_to_all(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="😂 Получить дозу чилла (мем)", callback_data="send_meme"))
    
    bot.reply_to(message, AUTO_REPLY_HTML, parse_mode="html", reply_markup=keyboard)

# Хэндлер на нажатие кнопки
@bot.callback_query_handler(func=lambda call: call.data == "send_meme")
def meme_callback(call):
    chat_id = call.message.chat.id
    
    bot.answer_callback_query(call.id, text="Загружаем мем... 😂")
    
    meme_url = get_random_meme_url()

    if meme_url:
        try:
            bot.send_document(chat_id, meme_url, caption="😂 Не кипятись, держи мем!")
        except Exception:
            bot.send_message(chat_id, "Мем не прогрузился, но ты всё равно отдохни! 😉")
    else:
        bot.send_message(chat_id, "Даже мемоделы ушли в отпуск... Попробуй позже! 😅")

# Точка входа
if __name__ == "__main__":
    keep_alive()            # Запускаем фейк-сервер
    bot.infinity_polling()  # Запускаем бота

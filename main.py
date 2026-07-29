import telebot
from telebot import types
import requests

TOKEN = "8730274244:AAFS2Ehm_knkwivPhPRI9lmEmt1Ml5S2erw"
bot = telebot.TeleBot(TOKEN)

# Настройка ответов
AUTO_REPLY_HTML = (
    "👋 <b>Я В ОТПУСКЕ И ТЕЛЕФОН НЕ БЕРУ.</b>\n\n"
    "По svim вопросам пишите тем, кто работает:\n"
    "• <b>Техника / разработка:</b> @ivan_dev\n"
    "• <b>Документы / оплаты:</b> @olga_paper\n"
    "• <b>Срочно / завал:</b> @support_team\n\n"
    "Вернусь — прочту (может быть). Удачи!"
)

# Функция для получения URL случайного мема (используем стабильный мем-API)
def get_random_meme_url():
    try:
        # Дергаем проверенный API мемов
        r = requests.get("https://meme-api.com/gimme", timeout=5)
        r.raise_for_status()
        data = r.json()
        
        # Если пришел nsfw (неприличный) мем, пробуем еще раз
        if data.get("nsfw"):
             return get_random_meme_url()
             
        return data.get("url")
    except:
        return None

# Хэндлер на любые сообщения
@bot.message_handler(content_types=['text', 'photo', 'sticker', 'voice', 'document'])
def reply_to_all(message):
    keyboard = types.InlineKeyboardMarkup()
    # Кнопку переименовали под мемы
    keyboard.add(types.InlineKeyboardButton(text="😂 Получить дозу чилла (мем)", callback_data="send_meme"))
    
    bot.reply_to(message, AUTO_REPLY_HTML, parse_mode="html", reply_markup=keyboard)

# Хэндлер на нажатие кнопки
@bot.callback_query_handler(func=lambda call: call.data == "send_meme")
def meme_callback(call):
    chat_id = call.message.chat.id
    
    bot.answer_callback_query(call.id, text="Загружаем мем... 😂")
    
    # 1. Получаем мем
    meme_url = get_random_meme_url()

    # 2. Отправляем или мем, или подбадривающий текст, если API лежит
    if meme_url:
        try:
            # API может вернуть mp4 или gif, telebot это нормально переварит
            bot.send_document(chat_id, meme_url, caption="😂 Не кипятись, держи мем!")
        except Exception as e:
            bot.send_message(chat_id, "Мем не прогрузился, но ты всё равно отдохни! 😉")
    else:
        bot.send_message(chat_id, "Даже мемоделы ушли в отпуск... Попробуй позже! 😅")

bot.infinity_polling()
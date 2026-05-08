import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# 1. Flask Веб-сервер (Render үчүн)
app = Flask('')

@app.route('/')
def home():
    return "Бот иштеп жатат!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Телеграм Боттун коду
TOKEN = "8747194233:AAE6SfJHAKuN0lciudl80FUBNrtyn8eIvFM"
bot = telebot.TeleBot(TOKEN)

SITE_URL = "https://mirzatesenjanov1-ship-it.github.io/Mugalim_AI"

levels_info = {
    "ru": [
        ("1️⃣ Механика (50 ₽)", "https://boosty.to/astrophysica/purchase/3915502?ssource=DIRECT&share=subscription_link"),
        ("2️⃣ Молекулярная физика (60 ₽)", "https://boosty.to/astrophysica/purchase/3915505?ssource=DIRECT&share=subscription_link"),
        ("3️⃣ Электродинамика (70 ₽)", "https://boosty.to/astrophysica/purchase/3915508?ssource=DIRECT&share=subscription_link"),
        ("4️⃣ Оптика (80 ₽)", "https://boosty.to/astrophysica/purchase/3915511?ssource=DIRECT&share=subscription_link"),
        ("5️⃣ Атомная физика (90 ₽)", "https://boosty.to/astrophysica/purchase/3915515?ssource=DIRECT&share=subscription_link"),
        ("6️⃣ Ядерная физика (100 ₽)", "https://boosty.to/astrophysica/purchase/3915516?ssource=DIRECT&share=subscription_link"),
        ("7️⃣ Квантовая механика (120 ₽)", "https://boosty.to/astrophysica/purchase/3915518?ssource=DIRECT&share=subscription_link"),
        ("8️⃣ Теория относительности (130 ₽)", "https://boosty.to/astrophysica/purchase/3915519?ssource=DIRECT&share=subscription_link"),
        ("9️⃣ Астрофизика (400 ₽)", "https://boosty.to/astrophysica/purchase/3915523?ssource=DIRECT&share=subscription_link")
    ],
    "ky": [
        ("1️⃣ Механика (50 ₽)", "https://boosty.to/astrophysica/purchase/3915502?ssource=DIRECT&share=subscription_link"),
        ("2️⃣ Молекулярдык физика (60 ₽)", "https://boosty.to/astrophysica/purchase/3915505?ssource=DIRECT&share=subscription_link"),
        ("3️⃣ Электродинамика (70 ₽)", "https://boosty.to/astrophysica/purchase/3915508?ssource=DIRECT&share=subscription_link"),
        ("4️⃣ Оптика (80 ₽)", "https://boosty.to/astrophysica/purchase/3915511?ssource=DIRECT&share=subscription_link"),
        ("5️⃣ Атомдук физика (90 ₽)", "https://boosty.to/astrophysica/purchase/3915515?ssource=DIRECT&share=subscription_link"),
        ("6️⃣ Ядролук физика (100 ₽)", "https://boosty.to/astrophysica/purchase/3915516?ssource=DIRECT&share=subscription_link"),
        ("7️⃣ Кванттык механика (120 ₽)", "https://boosty.to/astrophysica/purchase/3915518?ssource=DIRECT&share=subscription_link"),
        ("8️⃣ Салыштырмалуулук теориясы (130 ₽)", "https://boosty.to/astrophysica/purchase/3915519?ssource=DIRECT&share=subscription_link"),
        ("9️⃣ Астрофизика (400 ₽)", "https://boosty.to/astrophysica/purchase/3915523?ssource=DIRECT&share=subscription_link")
    ]
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
               InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_ky"))
    bot.send_message(message.chat.id, "Выберите язык / Тилди тандаңыз:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def main_menu(call):
    lang = call.data.split("_")[1]
    markup = InlineKeyboardMarkup(row_width=1)
    btn_levels = "📚 Уровни подписки" if lang == "ru" else "📚 Жазылуу деңгээлдери"
    btn_site = "🌐 Перейти на сайт Mugalim.AI" if lang == "ru" else "🌐 Mugalim.AI сайтына өтүү"
    markup.add(InlineKeyboardButton(btn_site, url=SITE_URL),
               InlineKeyboardButton(btn_levels, callback_data=f"show_levels_{lang}"))
    welcome = ("👋 Добро пожаловать!" if lang == "ru" else "👋 Кош келиңиз!")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_levels_"))
def list_levels(call):
    lang = call.data.split("_")[-1]
    markup = InlineKeyboardMarkup()
    for name, link in levels_info[lang]:
        markup.add(InlineKeyboardButton(name, url=link))
    back_btn = "⬅️ Назад" if lang == "ru" else "⬅️ Артка"
    markup.add(InlineKeyboardButton(back_btn, callback_data=f"lang_{lang}"))
    text = "🚀 Выберите уровень:" if lang == "ru" else "🚀 Деңгээлди тандаңыз:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)

# Ботту иштетүү
if __name__ == "__main__":
    keep_alive() # Веб-серверди иштетет
    print("🚀 Бот ишке кирди...")
    bot.polling(none_stop=True)

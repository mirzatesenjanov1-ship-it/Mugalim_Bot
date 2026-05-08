import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# Flask Веб-сервер (Render үчүн)
app = Flask('')

@app.route('/')
def home():
    return "Mugalim.AI боту иштеп жатат!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Телеграм Боттун коду (Жаңы токен менен)
TOKEN = "8747194233:AAE6SfJHAKuN0lciudl80FUBNrtyn8eIvFM"
bot = telebot.TeleBot(TOKEN)

SITE_URL = "https://mirzatesenjanov1-ship-it.github.io/Mugalim_AI"

# Жазылуулар боюнча маалымат
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
    
    if lang == "ru":
        text = (
            "<b>Mugalim.AI — ваш проводник в мир цифровой физики!</b>\n\n"
            "🌐 <b>На нашем сайте</b> вы найдете готовые планы уроков, интерактивные симуляции и виртуальные лаборатории, которые сделают обучение захватывающим.\n\n"
            "📚 <b>Подписка</b> открывает доступ к эксклюзивным материалам: от механики до астрофизики, созданным специально для современных учителей."
        )
        btn_site = "🌐 Перейти на сайт"
        btn_levels = "📚 Уровни подписки"
    else:
        text = (
            "<b>Mugalim.AI — санариптик физика дүйнөсүнө кош келиңиз!</b>\n\n"
            "🌐 <b>Биздин сайттан</b> сиз сабак пландарын, интерактивдүү оюндарды жана физикалык кубулуштарды түшүндүргөн виртуалдык лабораторияларды таба аласыз.\n\n"
            "📚 <b>Жазылуу деңгээлдери</b> сизге механикадан баштап астрофизикага чейинки тереңдетилген автордук материалдарга жол ачат."
        )
        btn_site = "🌐 Сайтка өтүү"
        btn_levels = "📚 Жазылуу деңгээлдери"

    markup.add(InlineKeyboardButton(btn_site, url=SITE_URL),
               InlineKeyboardButton(btn_levels, callback_data=f"show_levels_{lang}"))
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_levels_"))
def list_levels(call):
    lang = call.data.split("_")[-1]
    markup = InlineKeyboardMarkup()
    for name, link in levels_info[lang]:
        markup.add(InlineKeyboardButton(name, url=link))
    
    back_btn = "⬅️ Назад" if lang == "ru" else "⬅️ Артка"
    markup.add(InlineKeyboardButton(back_btn, callback_data=f"lang_{lang}"))
    
    text = (
        "<b>Выберите подходящий уровень доступа:</b>\n\n"
        "Ар бир деңгээл белгилүү бир тема боюнча тесттерди, видеолорду жана кошумча ресурстарды камтыйт." if lang == "ky" 
        else "<b>Выберите подходящий уровень доступа:</b>\n\nКаждый уровень содержит тесты, видео и дополнительные ресурсы по конкретной теме."
    )
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=text, reply_markup=markup, parse_mode='HTML')

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)

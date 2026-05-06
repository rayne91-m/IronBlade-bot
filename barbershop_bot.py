import os
"""
IRON BLADE — Telegram Bot для барбершопа
Установка: pip install pyTelegramBotAPI
Запуск: python barbershop_bot.py
"""

import telebot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
import datetime


TOKEN = os.environ.get("TOKEN")

BARBERSHOP = {
    "name": "IRON BLADE",
    "address": "Тверская ул., 15, Москва (м. Тверская)",
    "phone": "+7 (495) 123-45-67",
    "hours": "Ежедневно 10:00 — 22:00",
    "maps": "https://maps.google.com/?q=Тверская+15+Москва",
    "instagram": "https://instagram.com/ironblade_msk",
    "admin_chat_id": "CHAT_ID_ВЛАДЕЛЬЦА",  # Вставь сюда ID владельца для уведомлений
}

SERVICES = [
    {"name": "Классическая стрижка", "price": "1 500 ₽", "duration": "45 мин"},
    {"name": "Стрижка + борода", "price": "2 200 ₽", "duration": "60 мин"},
    {"name": "Моделирование бороды", "price": "900 ₽", "duration": "30 мин"},
    {"name": "Детская стрижка", "price": "1 000 ₽", "duration": "30 мин"},
    {"name": "Окрашивание", "price": "от 2 500 ₽", "duration": "90 мин"},
    {"name": "SPA для волос", "price": "1 800 ₽", "duration": "45 мин"},
]

MASTERS = [
    {"name": "Алексей Краснов", "spec": "Фейд, классика", "exp": "8 лет"},
    {"name": "Денис Морозов", "spec": "Классические стрижки", "exp": "5 лет"},
    {"name": "Иван Волков", "spec": "Стрижки + окрашивание", "exp": "6 лет"},
    {"name": "Сергей Петров", "spec": "Борода, уход", "exp": "4 года"},
]

TIMES = ["10:00", "11:00", "12:00", "13:00", "14:00",
         "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]

# ─── БОТ ─────────────────────────────────────────────────────────────────────

bot = telebot.TeleBot(TOKEN)

# Хранение состояний записи
bookings = {}  # {user_id: {step, service, master, date, time, name, phone}}


# ─── ГЛАВНОЕ МЕНЮ ─────────────────────────────────────────────────────────────

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("✂️ Записаться"),
        KeyboardButton("💰 Цены"),
        KeyboardButton("👨 Мастера"),
        KeyboardButton("📍 Адрес и часы"),
    )
    return kb


def main_inline():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✂️ Записаться", callback_data="book_start"),
        InlineKeyboardButton("💰 Прайс", callback_data="prices"),
        InlineKeyboardButton("👨 Мастера", callback_data="masters"),
        InlineKeyboardButton("📍 Контакты", callback_data="contacts"),
    )
    return kb


# ─── /START ───────────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start"])
def start(msg):
    name = msg.from_user.first_name or "друг"
    text = (
        f"Привет, {name}! 👋\n\n"
        f"*{BARBERSHOP['name']}* — мужской барбершоп в Москве.\n"
        f"Стрижки, борода, укладка. Работаем {BARBERSHOP['hours']}.\n\n"
        f"Выбери что тебя интересует:"
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown",
                     reply_markup=main_menu())


# ─── ТЕКСТОВЫЕ КОМАНДЫ ────────────────────────────────────────────────────────

@bot.message_handler(func=lambda m: m.text == "💰 Цены")
def show_prices_btn(msg):
    show_prices(msg.chat.id)

@bot.message_handler(func=lambda m: m.text == "👨 Мастера")
def show_masters_btn(msg):
    show_masters(msg.chat.id)

@bot.message_handler(func=lambda m: m.text == "📍 Адрес и часы")
def show_contacts_btn(msg):
    show_contacts(msg.chat.id)

@bot.message_handler(func=lambda m: m.text == "✂️ Записаться")
def book_start_btn(msg):
    start_booking(msg.chat.id, msg.from_user.id)


# ─── ПРАЙС ────────────────────────────────────────────────────────────────────

def show_prices(chat_id):
    lines = [f"*💰 ПРАЙС-ЛИСТ {BARBERSHOP['name']}*\n"]
    for s in SERVICES:
        lines.append(f"*{s['name']}*\n{s['price']} · {s['duration']}\n")
    lines.append("_Запись через кнопку ниже или по телефону._")
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✂️ Записаться", callback_data="book_start"))
    bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown", reply_markup=kb)


# ─── МАСТЕРА ──────────────────────────────────────────────────────────────────

def show_masters(chat_id):
    lines = [f"*👨 НАШИ МАСТЕРА*\n"]
    for m in MASTERS:
        lines.append(f"*{m['name']}*\n{m['spec']} · Опыт {m['exp']}\n")
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✂️ Записаться", callback_data="book_start"))
    bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown", reply_markup=kb)


# ─── КОНТАКТЫ ─────────────────────────────────────────────────────────────────

def show_contacts(chat_id):
    text = (
        f"*📍 {BARBERSHOP['name']}*\n\n"
        f"🗺 {BARBERSHOP['address']}\n"
        f"📞 {BARBERSHOP['phone']}\n"
        f"🕐 {BARBERSHOP['hours']}\n\n"
        f"[Открыть на карте]({BARBERSHOP['maps']})"
    )
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✂️ Записаться", callback_data="book_start"),
        InlineKeyboardButton("📞 Позвонить", url=f"tel:{BARBERSHOP['phone']}"),
    )
    bot.send_message(chat_id, text, parse_mode="Markdown",
                     reply_markup=kb, disable_web_page_preview=True)


# ─── ЗАПИСЬ: ПОШАГОВЫЙ ФЛОУ ───────────────────────────────────────────────────

def start_booking(chat_id, user_id):
    bookings[user_id] = {"step": "service"}
    kb = InlineKeyboardMarkup(row_width=1)
    for i, s in enumerate(SERVICES):
        kb.add(InlineKeyboardButton(
            f"{s['name']} — {s['price']}",
            callback_data=f"svc_{i}"
        ))
    bot.send_message(chat_id, "*✂️ Выбери услугу:*", parse_mode="Markdown", reply_markup=kb)


def ask_master(chat_id, user_id):
    bookings[user_id]["step"] = "master"
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Любой свободный мастер", callback_data="master_any"))
    for i, m in enumerate(MASTERS):
        kb.add(InlineKeyboardButton(
            f"{m['name']} · {m['spec']}",
            callback_data=f"master_{i}"
        ))
    bot.send_message(chat_id, "*👨 Выбери мастера:*", parse_mode="Markdown", reply_markup=kb)


def ask_date(chat_id, user_id):
    bookings[user_id]["step"] = "date"
    today = datetime.date.today()
    kb = InlineKeyboardMarkup(row_width=3)
    days = []
    for i in range(7):
        d = today + datetime.timedelta(days=i)
        label = d.strftime("%d.%m") + (" (сегодня)" if i == 0 else " (завтра)" if i == 1 else "")
        days.append(InlineKeyboardButton(label, callback_data=f"date_{d.strftime('%d.%m.%Y')}"))
    kb.add(*days)
    bot.send_message(chat_id, "*📅 Выбери дату:*", parse_mode="Markdown", reply_markup=kb)


def ask_time(chat_id, user_id):
    bookings[user_id]["step"] = "time"
    kb = InlineKeyboardMarkup(row_width=4)
    btns = [InlineKeyboardButton(t, callback_data=f"time_{t}") for t in TIMES]
    kb.add(*btns)
    bot.send_message(chat_id, "*🕐 Выбери время:*", parse_mode="Markdown", reply_markup=kb)


def ask_name(chat_id, user_id):
    bookings[user_id]["step"] = "name"
    bot.send_message(chat_id, "Введи своё *имя:*", parse_mode="Markdown")


def ask_phone(chat_id, user_id):
    bookings[user_id]["step"] = "phone"
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("📱 Отправить номер", request_contact=True))
    bot.send_message(chat_id,
        "Введи номер телефона или нажми кнопку ниже:",
        reply_markup=kb)


def confirm_booking(chat_id, user_id):
    b = bookings[user_id]
    svc = SERVICES[b["service"]]
    master = "Любой мастер" if b["master"] == "any" else MASTERS[b["master"]]["name"]

    text = (
        f"*✅ ПОДТВЕРДИ ЗАПИСЬ*\n\n"
        f"📋 Услуга: *{svc['name']}*\n"
        f"💰 Стоимость: *{svc['price']}*\n"
        f"👨 Мастер: *{master}*\n"
        f"📅 Дата: *{b['date']}*\n"
        f"🕐 Время: *{b['time']}*\n"
        f"👤 Имя: *{b['name']}*\n"
        f"📞 Телефон: *{b['phone']}*\n\n"
        f"Всё верно?"
    )
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_yes"),
        InlineKeyboardButton("❌ Отменить", callback_data="confirm_no"),
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)


def finish_booking(chat_id, user_id):
    b = bookings[user_id]
    svc = SERVICES[b["service"]]
    master = "Любой мастер" if b["master"] == "any" else MASTERS[b["master"]]["name"]

    # Сообщение клиенту
    bot.send_message(
        chat_id,
        f"*🎉 Запись подтверждена!*\n\n"
        f"Ждём тебя *{b['date']}* в *{b['time']}*\n"
        f"📍 {BARBERSHOP['address']}\n\n"
        f"За час до визита пришлём напоминание.\n"
        f"Если планы изменятся — напиши сюда.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

    # Уведомление владельцу
    if BARBERSHOP["admin_chat_id"] != "CHAT_ID_ВЛАДЕЛЬЦА":
        admin_text = (
            f"🆕 *НОВАЯ ЗАПИСЬ*\n\n"
            f"📋 {svc['name']} — {svc['price']}\n"
            f"👨 Мастер: {master}\n"
            f"📅 {b['date']} в {b['time']}\n"
            f"👤 {b['name']}\n"
            f"📞 {b['phone']}\n"
            f"🆔 user_id: {user_id}"
        )
        try:
            bot.send_message(BARBERSHOP["admin_chat_id"], admin_text, parse_mode="Markdown")
        except Exception:
            pass

    del bookings[user_id]


# ─── CALLBACK HANDLERS ────────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = call.data

    bot.answer_callback_query(call.id)

    # Главное меню из inline
    if data == "prices":
        show_prices(chat_id)
    elif data == "masters":
        show_masters(chat_id)
    elif data == "contacts":
        show_contacts(chat_id)
    elif data == "book_start":
        start_booking(chat_id, user_id)

    # Запись — услуга
    elif data.startswith("svc_"):
        idx = int(data.split("_")[1])
        if user_id not in bookings:
            bookings[user_id] = {}
        bookings[user_id]["service"] = idx
        bot.edit_message_text(
            f"✅ Выбрано: *{SERVICES[idx]['name']}*",
            chat_id, call.message.message_id,
            parse_mode="Markdown"
        )
        ask_master(chat_id, user_id)

    # Запись — мастер
    elif data.startswith("master_"):
        val = data.split("_")[1]
        bookings[user_id]["master"] = "any" if val == "any" else int(val)
        master_name = "Любой мастер" if val == "any" else MASTERS[int(val)]["name"]
        bot.edit_message_text(
            f"✅ Мастер: *{master_name}*",
            chat_id, call.message.message_id,
            parse_mode="Markdown"
        )
        ask_date(chat_id, user_id)

    # Запись — дата
    elif data.startswith("date_"):
        date_str = data.split("_")[1]
        bookings[user_id]["date"] = date_str
        bot.edit_message_text(
            f"✅ Дата: *{date_str}*",
            chat_id, call.message.message_id,
            parse_mode="Markdown"
        )
        ask_time(chat_id, user_id)

    # Запись — время
    elif data.startswith("time_"):
        time_str = data.split("_")[1]
        bookings[user_id]["time"] = time_str
        bot.edit_message_text(
            f"✅ Время: *{time_str}*",
            chat_id, call.message.message_id,
            parse_mode="Markdown"
        )
        ask_name(chat_id, user_id)

    # Подтверждение
    elif data == "confirm_yes":
        finish_booking(chat_id, user_id)

    elif data == "confirm_no":
        if user_id in bookings:
            del bookings[user_id]
        bot.send_message(chat_id, "Запись отменена. Возвращайся когда будешь готов 👌",
                         reply_markup=main_menu())


# ─── ТЕКСТОВЫЕ СООБЩЕНИЯ (ввод имени и телефона) ──────────────────────────────

@bot.message_handler(content_types=["contact"])
def handle_contact(msg):
    user_id = msg.from_user.id
    if user_id in bookings and bookings[user_id].get("step") == "phone":
        phone = msg.contact.phone_number
        bookings[user_id]["phone"] = phone
        confirm_booking(msg.chat.id, user_id)


@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    user_id = msg.from_user.id
    text = msg.text.strip()

    if user_id not in bookings:
        # Неизвестная команда — показать меню
        bot.send_message(msg.chat.id,
            "Выбери действие в меню ниже 👇",
            reply_markup=main_menu())
        return

    step = bookings[user_id].get("step")

    if step == "name":
        if len(text) < 2:
            bot.send_message(msg.chat.id, "Введи настоящее имя.")
            return
        bookings[user_id]["name"] = text
        ask_phone(msg.chat.id, user_id)

    elif step == "phone":
        # Ручной ввод телефона
        digits = "".join(c for c in text if c.isdigit())
        if len(digits) < 10:
            bot.send_message(msg.chat.id, "Введи корректный номер телефона.")
            return
        bookings[user_id]["phone"] = text
        confirm_booking(msg.chat.id, user_id)


# ─── ЗАПУСК ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Бот {BARBERSHOP['name']} запущен...")
    bot.infinity_polling()

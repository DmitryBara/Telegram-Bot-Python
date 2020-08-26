from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_share_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Поделиться мемом", callback_data="cb_share"))
    return markup


def gen_confirm_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
               InlineKeyboardButton("Нет", callback_data="cb_no"))
    return markup


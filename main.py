import os
import telebot

from src.markups import gen_share_markup, gen_confirm_markup
from src.services import save_image, edit_image
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
chat_for_resend = os.getenv('CHAT_FOR_RESEND')


@bot.message_handler(content_types=["text"])
def answer_to_text(message):
    bot.send_message(message.chat.id, "Пришли мне фото!!!!")


@bot.message_handler(content_types=['photo'])
def answer_to_photo(message):
    bot.send_message(message.chat.id, "Происходит магия...")
    user_img = save_image(bot, message)
    new_img = edit_image(bot, user_img)
    bot.send_photo(message.chat.id, new_img, reply_markup=gen_share_markup())
    return "Return for test"


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_share":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, 'Поделиться мемом с другими пользователями?',
                         reply_to_message_id=call.message.message_id, reply_markup=gen_confirm_markup())
    elif call.data == "cb_yes":
        try:
            photo_id = call.message.reply_to_message.photo[0].file_id
            bot.send_photo(chat_for_resend, photo_id)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(call.message.chat.id, 'Этот мем теперь доступен всем!',
                             reply_to_message_id=call.message.reply_to_message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            bot.send_message(call.message.chat.id, 'Возникла проблема :(')
            print('***Error while bot trying to share image in other chat***\n')
            print(e)
    elif call.data == "cb_no":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.reply_to_message.message_id,
                                      reply_markup=gen_share_markup())
        bot.delete_message(call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    print('Bot is running now...')
    bot.infinity_polling()
import os, datetime, random, textwrap, time

import telebot
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()
img_folder = os.getenv('IMG_FOLDER')
phrase_file_dir = os.getenv('PHRASE_FILE_DIR')
font_file_dir = os.getenv('FONT_DIR')

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

phrase_file = open(phrase_file_dir, 'r')
phrase_list = phrase_file.readlines()
phrase_file.close()


def save_image(bot, message):
    dt = datetime.datetime.fromtimestamp(message.date)
    img_name = dt.strftime('%Y-%m-%d_%H:%M_<') + str(message.from_user.id) + '>.jpg'
    img_dir = img_folder + img_name

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(img_dir, 'wb') as user_img:
        user_img.write(downloaded_file)
    return user_img


def edit_image(bot, user_img):
    phrase = random.choice(phrase_list).rstrip()
    new_img = Image.open(user_img.name)
    imgDrawer = ImageDraw.Draw(new_img)

    W, H = new_img.size  # width, height for image
    max_w = int(os.getenv('MAX_WIDTH_OF_TEXT')) * 0.01 * W
    max_h = int(os.getenv('MAX_HEIGHT_OF_TEXT')) * 0.01 * H

    size = int(H * 0.1)  # starting size of text
    font = ImageFont.truetype(font_file_dir, size)  # create font with this size
    fill = (0, 0, 0, 0)  # color of text shadow
    w, h = imgDrawer.textsize(phrase, font=font)  # w, h - total width and height of all phrase

    if w < max_w:  # if could put all phrase in one line. h < max_h automatically
        x = (W - w) / 2
        y = H - h - 0.03 * H
        imgDrawer.text((x - 1, y - 1), phrase, font=font, fill=fill)
        imgDrawer.text((x + 1, y - 1), phrase, font=font, fill=fill)
        imgDrawer.text((x - 1, y + 1), phrase, font=font, fill=fill)
        imgDrawer.text((x + 1, y + 1), phrase, font=font, fill=fill)
        imgDrawer.text((x, y), phrase, font=font)

    else:
        while w > max_w or h > max_h:

            symbols_in_one_line = int(len(phrase) / (w / max_w))  # approximately length of one line
            para = textwrap.wrap(phrase, width=symbols_in_one_line)  # all created lines with this length

            total_h = H * 0.03  # accumulate margin bottom on this iteration
            total_w = []  # list of width from every line on this iteration
            font = ImageFont.truetype(font_file_dir, size)  # change font size on this iteration

            for line in para: # check future size of text block
                wl, hl = imgDrawer.textsize(line, font=font)  # wl - width of line, hl - height of line
                total_h += hl
                total_w.append(wl)
            h = total_h
            w = max(total_w)
            size = int(size * 0.98)  # decrease font size on 2%

        # After exit from while loop could draw on image. Use data from last while iteration.
        total_h = H * 0.03
        font = ImageFont.truetype(font_file_dir, size)
        para.reverse()
        for line in para:
            wl, hl = imgDrawer.textsize(line, font=font)  # wl - width of line, hl - height of line
            x = (W - wl) / 2
            y = (H - hl - total_h)
            imgDrawer.text((x - 1, y - 1), line, font=font, fill=fill)  # shadow for text (as on 51-54 lines)
            imgDrawer.text((x + 1, y - 1), line, font=font, fill=fill)  # go away from DRY princips for code readability
            imgDrawer.text((x - 1, y + 1), line, font=font, fill=fill)
            imgDrawer.text((x + 1, y + 1), line, font=font, fill=fill)
            imgDrawer.text((x, y), line, font=font)
            total_h += hl
        # time.sleep(15)
    return new_img

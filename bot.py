# import logging
# import typing
# from io import BytesIO
# import requests
# from PIL import Image
# import secrets
# import cv2
# import model
# from telegram import Update, PhotoSize
# from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
#     Filters, Updater
#
# logging.basicConfig(
#     format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
#     level=logging.INFO)
#
# logger = logging.getLogger(__name__)
#
# updater = Updater(token=secrets.BOT_TOKEN, use_context=True)
# dispatcher = updater.dispatcher
#
# users = {}
#
#
# def to_puzzle(image1_str, image2_str):
#     good_image = model.paste_face(image1_str, image2_str)
#     print(good_image)
#     # file = requests.get(image)
#     # im = Image.open(BytesIO(file.content))
#     # im.save('testimage.jpg')
#     # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     # img = cv2.imread('testimage.jpg')
#     # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#     # print(faces[0][1])
#     # img1 = Image.open('testimage.jpg')
#     # part = img1.crop((faces[0][0], faces[0][1], faces[0][0] + faces[0][2], faces[0][1] + faces[0][2]))
#     # new_image = Image.new('RGBA', (faces[0][2], faces[0][3]))
#     # new_image.paste(part, (0, 0, faces[0][2], faces[0][2]))
#     # new_image.save('new1.png')
#     return good_image
#
#
# def start(update: Update, context: CallbackContext):
#     global users
#     chat_id = update.effective_chat.id
#     user_id = update.effective_user.id
#     users[user_id] = [(0, 0), (0, 0), 'to go']
#     logger.info(f"> Start chat #{chat_id}")
#     context.bot.send_message(chat_id=chat_id,
#                              text="Add two pictures to swap")
#
#
# count = 0
#
#
# def photo(update: Update, context: CallbackContext, photo1=[]):
#     chat_id = update.effective_chat.id
#     user_id = update.effective_user.id
#     photos: typing.List[PhotoSize] = update.message.photo
#     print(update.message.photo)
#     print(len(photos))
#     global count
#     if (count == 0):
#         count += 1
#         print("hisadfojsdokdslakf")
#         print(photos)
#         f = photos[0].get_file()
#         print(f)
#         path_id1 = f['file_path']
#         print(path_id1)
#         file = requests.get(path_id1)
#         im1 = Image.open(BytesIO(file.content))
#         im1.save('photo1.png')
#     else:
#         g = photos[0].get_file()
#         print(g)
#         path_id2 = g['file_path']
#         print(path_id2)
#         file = requests.get(path_id2)
#         im2 = Image.open(BytesIO(file.content))
#         im2.save('photo2.png')
#         result = to_puzzle('photo1.png', 'photo2.png')
#         print(result)
#         context.bot.send_photo(chat_id=chat_id, photo=open(f'{result}', 'rb'))
#
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
#
# location_handler = MessageHandler(Filters.photo, photo, pass_user_data=True)
# dispatcher.add_handler(location_handler)
#
# logger.info("* Start polling...")
# updater.start_polling()  # Starts polling in a background thread.
# updater.idle()  # Wait until Ctrl+C is pressed
# logger.info("* Bye!")
# # def main():
# #     print(secrets.BOT_TOKEN)
# #     # YOUR BOT HERE
# #
# #
# # if __name__ == '__main__':
# #     main()
import logging
from pymongo import MongoClient
from model import paste_face
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater

import secret
# import how_old


logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret.TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text="Hello! Enter a celebrity name and I'll tell you her age!")


def respond(update: Update, context: CallbackContext):
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = text
    context.bot.send_message(chat_id=update.message.chat_id, text=response)

def image(update: Update, context: CallbackContext):
    user = {}
    text = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    client = MongoClient()
    db = client.get_database("picture_by_user")
    results = db.get_collection("user_picture")
    photos: typing.List[PhotoSize] = update.message.photo
    f = photos[0].get_file()
    user['user_id'] = f'{user_id}'
    user['file_path'] = f['file_path']
    user["kind"] = f['file_path']
    results.insert_one(user)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

image_handler = MessageHandler(Filters.photo, image, pass_user_data=True)
dispatcher.add_handler(image_handler)





logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
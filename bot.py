import logging
from io import BytesIO

import requests
from PIL import Image
from pymongo import MongoClient
from model import paste_face
import model
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler
import secret

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret.TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text="Welcome! to start please upload a profile picture")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    print(text)
    # model.buttuns(update)
    # response = text
    # return_pic = paste_face('./picture/user_pic.jpg', f'./picture/{text}.jpg')
    # context.bot.send_photo(chat_id=chat_id, photo=open(return_pic, 'rb'))


user_picture = {}


def image(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    model.users_pic[user_id] = './picture/user_pic.jpg'
    # logger.info(f"= Got on chat #{chat_id}: {text!r}")
    reply_markup = model.buttuns(update)
    update.message.reply_text('Please choose your character:', reply_markup=reply_markup)
    # context.bot.send_message(chat_id=update.message.chat_id,  text = response )
    photos: typing.List[PhotoSize] = update.message.photo
    f = photos[0].get_file()
    file = requests.get(f['file_path'])
    im = Image.open(BytesIO(file.content))
    im.save('./picture/user_pic.jpg')

    # user = {}
    # text = update.message.text
    # chat_id = update.effective_chat.id
    # user_id = update.effective_user.id
    # client = MongoClient()
    # db = client.get_database("picture_by_user")
    # results = db.get_collection("user_picture")
    # photos: typing.List[PhotoSize] = update.message.photo
    # f = photos[0].get_file()
    # user['user_id'] = f'{user_id}'
    # user['file_path'] = f['file_path']
    # user["kind"] = f['file_path']
    # results.insert_one(user)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

image_handler = MessageHandler(Filters.photo, igite, pass_user_data=True)
dispatcher.add_handler(image_handler)

dispatcher.add_handler(CallbackQueryHandler(model.button))
# dispatcher.add_handler(CallbackQueryHandler(respond))


logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")

import logging
from io import BytesIO
import random
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

chats = model.get_mongo_storage("Users_faces")

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text="Welcome! to start please upload a profile picture")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    print(text)



def image(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    num = random.randrange(355585965444, 555585965444)
    model.add_item(chats, chat_id, num)

    reply_markup = model.buttuns(update)

    photos: typing.List[PhotoSize] = update.message.photo
    f = photos[0].get_file()
    file = requests.get(f['file_path'])
    im = Image.open(BytesIO(file.content))
    im.save(f'./picture/{num}.jpg')
    update.message.reply_text('Please choose your character:', reply_markup=reply_markup)



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

image_handler = MessageHandler(Filters.photo, image, pass_user_data=True)
dispatcher.add_handler(image_handler)

dispatcher.add_handler(CallbackQueryHandler(model.button))
# dispatcher.add_handler(CallbackQueryHandler(respond))


logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")

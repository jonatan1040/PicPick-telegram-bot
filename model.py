import cv2
from PIL import Image
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater
from telegram import Update
# מוצא איפה הפנים נמצאות בתמונה לפי פיקסלים
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def find_face(image):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces


# מריץ את הפנקציה של מציאת הפנים על שתי התמונות ןמדביק את הפנים של התמונה הראשונה על השנייה
def paste_face(image1, image2):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    faces = find_face(image1)
    faces_to_paste = find_face(image2)
    part = img1.crop((faces[0][0], faces[0][1], faces[0][0] + faces[0][2], faces[0][1] + faces[0][2]))
    part1 = part.resize((faces_to_paste[0][2], faces_to_paste[0][3]))
    img2.paste(part1, (faces_to_paste[0][0], faces_to_paste[0][1], faces_to_paste[0][0] + faces_to_paste[0][2],
                       faces_to_paste[0][1] + faces_to_paste[0][3]))
    img2.save('./picture/new2.png')
    return './picture/new2.png'


def buttuns(update):
    keyboard = [
        [
            InlineKeyboardButton("Astronaut", callback_data='Astronaut'),
            InlineKeyboardButton("Pilot", callback_data='Pilot')
        ],

        [
            InlineKeyboardButton("Dancer", callback_data='Dancer'),
            InlineKeyboardButton("Ballerina", callback_data='Ballerina')
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


users_pic = {}


def button(update, context):
    global choose
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query
    return_pic = paste_face(f'{users_pic[user_id]}', f'./picture/{query.data}.jpg')
    context.bot.send_photo(chat_id=chat_id, photo=open(return_pic, 'rb'))
    reply_markup = buttuns(update)
    context.bot.send_message(chat_id=chat_id, text='Choose another h=', reply_markup=reply_markup)

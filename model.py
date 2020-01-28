from pymongo.collection import Collection
import cv2
import pymongo
from PIL import Image
from pymongo import MongoClient
# מוצא איפה הפנים נמצאות בתמונה לפי פיקסלים
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import numpy as np
from PIL import Image, ImageDraw


def find_face(image):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if faces == ():
        faces = [[10, 100, 147, 147]]
    return faces


# מריץ את הפנקציה של מציאת הפנים על שתי התמונות ןמדביק את הפנים של התמונה הראשונה על השנייה
def paste_face(image2, chat_id):
    items = list_items(chats, chat_id)
    img2: Image.Image = Image.open(image2)
    img2.putalpha(255)
    faces_to_paste = find_face(image2)
    parts = []
    print(items)
    print(type(items))
    for j in range(len(faces_to_paste)):
        faces = find_face(f'./picture/{items[len(items) - 1 - j]}')
        print(faces)
        # if faces != ():
        print('test1')
        part = Image.open(f'./picture/{items[len(items) - 1 - j]}').crop(
            (faces[0][0], faces[0][1]-20, faces[0][0] + faces[0][2], faces[0][1]-20 + faces[0][2]+20))
        part_circled = to_circle(part)
        print(part_circled.format, part_circled.mode)
        parts.append(part_circled)

    for i in range(len(faces_to_paste)):
        face = faces_to_paste[i]
        part1 = parts[i].resize((face[2]+10, face[3]+20))
        img2.paste(part1, (face[0]-5, face[1]-10, face[0] + face[2]+5, face[1] + face[3]+10), mask=part1)
    img2.save('./picture/new2.png')
    return './picture/new2.png'


def buttuns(update):
    keyboard = [
        [
            InlineKeyboardButton("Astronaut", callback_data='Astronaut'),
            InlineKeyboardButton("Pilot", callback_data='Pilot'),
            InlineKeyboardButton("Messi", callback_data='Messi')

        ],

        [
            InlineKeyboardButton("Dancer", callback_data='Dancer'),
            InlineKeyboardButton("Ballerina", callback_data='Ballerina')
        ],
        [
            InlineKeyboardButton("Group1", callback_data='Group1'),
            InlineKeyboardButton("Group2", callback_data='Group2'),
            InlineKeyboardButton("Group3", callback_data='Group3'),

        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def button(update, context):
    global choose
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query
    print(query.data)
    items = list_items(chats, chat_id)
    return_pic = paste_face(f'./picture/{query.data}.jpg', update.effective_chat.id)
    context.bot.send_photo(chat_id=chat_id, photo=open(return_pic, 'rb'))
    reply_markup = buttuns(update)
    context.bot.send_message(chat_id=chat_id, text='Choose another character:', reply_markup=reply_markup)


def get_mongo_storage(dbname):
    client = MongoClient()
    db = client.get_database(dbname)
    coll = db.get_collection("chats")
    coll.create_index([
        ('chat_id', pymongo.ASCENDING),
    ], unique=True)
    return coll


chats = get_mongo_storage("Users_faces")


def add_item(chats, chat_id, num):
    # {chat_id: 7213125, items: ['milk', 'coffee', 'banana']}
    chats.update_one({'chat_id': chat_id}, {
        "$push": {'items': f'{num}.jpg'}
    }, upsert=True)


def list_items(coll: Collection, chat_id):
    d = coll.find_one({'chat_id': chat_id})
    return d['items']


def to_circle(pic):
    img = pic.convert("RGBA")
    npImage = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    # npImage = np.dstack((npImage, npAlpha))
    npImage[:, :, 3] = npAlpha

    # Save with alpha
    # Image.fromarray(npImage).save('result.png')

    return Image.fromarray(npImage)

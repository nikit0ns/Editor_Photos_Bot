# Імпорти потрібних бібліотек
import asyncio
import os
import os.path
import numpy as np
import cv2
import sys
from PIL import Image

from aiogram.client import bot
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject, Text
from aiogram.enums import ParseMode
from aiogram.types import URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, FSInputFile, CallbackQuery


API_TOKEN = '...' #Сюди ви пишете свій токен. Дізнатися його можна дізнатися в @BotFather
JSON_FILE = 'photos.json'
logging.basicConfig(level = logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#Головна клавіатура та для кожної функції
main_buttons = [
        [
            types.InlineKeyboardButton(text = "🖍 Кольори", callback_data = "btn_colors"), 
            types.InlineKeyboardButton(text = "🗂 Фільтр", callback_data = "btn_filter")
        ],
        [
            types.InlineKeyboardButton(text = "⚙️ Налаштування", callback_data = "btn_settings"),  
            types.InlineKeyboardButton(text = "📐 Поворот", callback_data = "btn_rotate")
        ],
        [
            types.InlineKeyboardButton(text = "📥 Завантажити", callback_data = "btn_download")
        ]
    ]
main_keyboard = types.InlineKeyboardMarkup(inline_keyboard = main_buttons)

colors_buttons = [
        [
            types.InlineKeyboardButton(text = "Жовтий", callback_data = "btn_yellow"), 
            types.InlineKeyboardButton(text = "Красний", callback_data = "btn_red")
        ],
        [
            types.InlineKeyboardButton(text = "Синій", callback_data = "btn_blue"), 
            types.InlineKeyboardButton(text = "Зелений", callback_data = "btn_green")
        ],
        [
            types.InlineKeyboardButton(text = "📚 Головне меню", callback_data = "btn_main_menu")
        ]
    ]
colors_keyboard = types.InlineKeyboardMarkup(inline_keyboard = colors_buttons)

filter_buttons = [
        [
            types.InlineKeyboardButton(text = "HDR", callback_data = "btn_hdr"), 
            types.InlineKeyboardButton(text = "Сепія", callback_data = "btn_sepia")
        ],
        [
            types.InlineKeyboardButton(text = "Відтінки сірого", callback_data = "btn_grey"), 
            types.InlineKeyboardButton(text = "Інверсія", callback_data = "btn_invert")
        ],
        [
            types.InlineKeyboardButton(text = "📚 Головне меню", callback_data = "btn_main_menu")
        ]
]
filter_keyboard = types.InlineKeyboardMarkup(inline_keyboard = filter_buttons)

settings_buttons = [
        [
            types.InlineKeyboardButton(text = "Яскравість", callback_data = "btn_brightness"), 
            types.InlineKeyboardButton(text = "Контрастність", callback_data = "btn_contrast")
        ],
        [
            types.InlineKeyboardButton(text = "Насиченість", callback_data = "btn_saturation"), 
            types.InlineKeyboardButton(text = "Границі", callback_data = "btn_edge")
        ],
        [
            types.InlineKeyboardButton(text = "📚 Головне меню", callback_data = "btn_main_menu")
        ]
    ]
settings_keyboard = types.InlineKeyboardMarkup(inline_keyboard = settings_buttons)

rotate_buttons = [
        [
            types.InlineKeyboardButton(text = "90°", callback_data = "btn_90"), 
            types.InlineKeyboardButton(text = "-90°", callback_data = "btn_minus_90")
        ],
        [
            types.InlineKeyboardButton(text = "180°", callback_data = "btn_180"), 
            types.InlineKeyboardButton(text = "-180°", callback_data = "btn_minus_180")
        ],
        [
            types.InlineKeyboardButton(text = "📚 Головне меню", callback_data = "btn_main_menu")
        ]
    ]
rotate_keyboard = types.InlineKeyboardMarkup(inline_keyboard = rotate_buttons)

download_buttons = [
        [
            types.InlineKeyboardButton(text = "PNG", callback_data = "btn_png"), 
            types.InlineKeyboardButton(text = "JPG", callback_data = "btn_jpg")
        ],
        [
            types.InlineKeyboardButton(text = "WEbP", callback_data = "btn_webp"),  
            types.InlineKeyboardButton(text = "TIFF", callback_data = "btn_tiff")
        ],
        [
            types.InlineKeyboardButton(text = "📚 Головне меню", callback_data = "btn_main_menu")
        ]
    ]
download_keyboard = types.InlineKeyboardMarkup(inline_keyboard = download_buttons)


#---------------------------------------------------------------------------------------------------------------------
# Завантажуємо дані з JSON-файлу
def load_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


#---------------------------------------------------------------------------------------------------------------------
# Зберігаємо дані в JSON-файлі
def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file)


chat_counts = load_data()


#---------------------------------------------------------------------------------------------------------------------
#Головні команди бота
@dp.message(Command(commands = ['start']))
async def cmd_start(message: types.Message):
    await message.answer('🖼 <b>Editor Photos Bot</b> — це <b>зручний інструмент</b> для швидкого і якісного <b>редагування</b> ваших <b>фотографій</b> прямо в <b>Telegram</b>. <b>Завдяки</b> цьому <b>боту</b>, у вас є <b>можливість перетворити</b> звичайні <b>фотографії</b> на <b>витвори мистецтва</b> всього за <b>кілька кроків</b>. \n\n📚 <b>Основні функції</b>: \n\n✂️ Обрізати; \n🗂 Фільтр; \n⚙️ Налаштування; \n📐 Поворот.\n\n🗒 <b>Команди бота</b>:\n\n🖥 Запустити бота - <b>/start</b>\n⁉️ Технічна підтримка - <b>/help</b>\n\n⚠️ <b>Для обробки надішліть фото (не документом)</b>')

@dp.message(Command(commands = ['help']))
async def cmd_help(message: types.Message):
    await message.answer("⁉️<b> Якщо у вас є проблеми.</b> \n"
                         "✉️ <b>Напишіть мені</b> <a href = 'https://t.me/nikit0ns'>@nikit0ns</a><b>.</b>", 
                         disable_web_page_preview = True)

@dp.message(F.photo)
async def handle_message(message: types.Message, state):
    data = await state.get_data()
    if data.get("last_message_id"):
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=data.get("last_message_id"))
        except:
            pass    
        
    chat_id = str(message.chat.id)  # Ключі у JSON повинні бути рядками
    if chat_id not in chat_counts:
        chat_counts[chat_id] = {"photo": None, "last_msg_id": None}
    
    if chat_counts[chat_id]["last_msg_id"]:
        try: 
            os.remove(chat_counts[chat_id]["photo"])
        except Exception as e:
            print(e)

    path = f"{message.from_user.id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )

    image = FSInputFile(
        path=path
    ) 
    sent_message =  await bot.send_photo(chat_id, photo = image,parse_mode = ParseMode.MARKDOWN, reply_markup = main_keyboard)
    chat_counts[chat_id]["last_msg_id"] = sent_message.message_id
    chat_counts[chat_id]["photo"] = path
    save_data(chat_counts)
    await state.update_data(last_message_id = sent_message.message_id)
    await message.delete()

#---------------------------------------------------------------------------------------------------------------------
@dp.callback_query(Text("btn_main_menu"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=main_keyboard)

@dp.callback_query(Text("btn_colors"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=colors_keyboard)

@dp.callback_query(Text("btn_filter"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=filter_keyboard)

@dp.callback_query(Text("btn_settings"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=settings_keyboard)

@dp.callback_query(Text("btn_rotate"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=rotate_keyboard)

@dp.callback_query(Text("btn_download"))
async def callback_answer(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=download_keyboard)


#---------------------------------------------------------------------------------------------------------------------
#Функції для Кольорів
@dp.callback_query(Text("btn_yellow"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = np.copy(src)
    image[:, :, 0] = 0  
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=colors_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


@dp.callback_query(Text("btn_red"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = np.copy(src)
    image[:, :, 0] = 0  # Set green channel to 0
    image[:, :, 1] = 0  # Set red channel to 0
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=colors_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


@dp.callback_query(Text("btn_blue"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = np.copy(src)
    image[:, :, 1] = 0  # Set green channel to 0
    image[:, :, 2] = 0  # Set red channel to 0
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=colors_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


@dp.callback_query(Text("btn_green"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = np.copy(src)
    image[:, :, 0] = 0  # Set blue channel to 0
    image[:, :, 2] = 0  # Set red channel to 0
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image),
            reply_markup=colors_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

#---------------------------------------------------------------------------------------------------------------------
#Функції для Фільтра
@dp.callback_query(Text("btn_hdr"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.detailEnhance(src, sigma_s = 12, sigma_r = 0.15)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=filter_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_sepia"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = np.array(src, dtype = np.float64)
    image = cv2.transform(image, np.matrix([[0.272, 0.543, 0.131], 
                                            [0.349, 0.686, 0.168], 
                                            [0.393, 0.769, 0.189]]))
    image[np.where(image > 255)] = 255
    image = np.array(image, dtype = np.uint8)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=filter_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_grey"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id,
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=filter_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_invert"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.bitwise_not(src)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image),
            reply_markup=filter_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


#---------------------------------------------------------------------------------------------------------------------
#Функції для Налаштування
@dp.callback_query(Text("btn_brightness"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.convertScaleAbs(src, beta = 25)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=settings_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_contrast"))
async def callback_answer(callback: CallbackQuery):
    alpha = 1.5  
    beta = 1.2
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.convertScaleAbs(src, alpha, beta)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=settings_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

def adjust_saturation(image, saturation_factor):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image = np.array(hsv_image, dtype=np.float64)
    hsv_image[:, :, 1] = hsv_image[:, :, 1] * saturation_factor
    hsv_image[:, :, 1][hsv_image[:, :, 1] > 255] = 255
    hsv_image = np.array(hsv_image, dtype=np.uint8)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

@dp.callback_query(Text("btn_saturation"))
async def callback_answer(callback: CallbackQuery):
    saturation_factor = 1.2
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = adjust_saturation(src, saturation_factor)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=settings_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


@dp.callback_query(Text("btn_edge"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    park = cv2.cvtColor(src,cv2.COLOR_BGR2RGB)
    image = cv2.Canny(park,100,200)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=settings_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


#---------------------------------------------------------------------------------------------------------------------
#Функції для Поворота 
@dp.callback_query(Text("btn_90"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.rotate(src, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=rotate_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_minus_90"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.rotate(src, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=rotate_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_180"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.rotate(src, cv2.ROTATE_180)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id, 
            media=types.InputMediaPhoto(media=updated_image), 
            reply_markup=rotate_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')

@dp.callback_query(Text("btn_minus_180"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    src = cv2.imread(path)
    image = cv2.rotate(src, cv2.ROTATE_180)
    cv2.imwrite(path, image)
    updated_image = FSInputFile(path=path)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id, media=types.InputMediaPhoto(media=updated_image), reply_markup=rotate_keyboard)
    except:
        callback.answer('❌ <b>Помилка під час обробки вашого фото.</b>')


#---------------------------------------------------------------------------------------------------------------------
#Функції для Завантаження
@dp.callback_query(Text("btn_png"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    png_image = Image.open(path)
    jpg_image = png_image.convert('RGB')
    jpg_image.save(f"{path[:-4]}.png")
    updated_image = FSInputFile(path=f"{path[:-4]}.png")
    await callback.message.answer_document(document=updated_image)
    await callback.message.delete()
    os.remove(path=f"{path[:-4]}.png")

@dp.callback_query(Text("btn_jpg"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    png_image = Image.open(path)
    jpg_image = png_image.convert('RGB')
    jpg_image.save(f"{path[:-4]}.jpg")
    updated_image = FSInputFile(path=f"{path[:-4]}.jpg")
    await callback.message.answer_document(document=updated_image)
    await callback.message.delete()

@dp.callback_query(Text("btn_webp"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    png_image = Image.open(path)
    jpg_image = png_image.convert('RGB')
    jpg_image.save(f"{path[:-4]}.webp")
    updated_image = FSInputFile(path=f"{path[:-4]}.webp")
    await callback.message.answer_document(document=updated_image)
    await callback.message.delete(path=f"{path[:-4]}.webp")
    os.remove(path=f"{path[:-4]}.webp")

@dp.callback_query(Text("btn_tiff"))
async def callback_answer(callback: CallbackQuery):
    path = chat_counts[str(callback.message.chat.id)]["photo"]
    png_image = Image.open(path)
    jpg_image = png_image.convert('RGB')
    jpg_image.save(f"{path[:-4]}.tiff")
    updated_image = FSInputFile(path=f"{path[:-4]}.tiff")
    await callback.message.answer_document(document=updated_image)
    await callback.message.delete()
    os.remove(path=f"{path[:-4]}.tiff")



@dp.message()  
async def handle_text(message: types.Message):
    await message.answer('❌ Помилка. Будь ласка, надішліть фотографію')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

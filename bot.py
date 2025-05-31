import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import TOKEN
from utils.pdf_generator import generate_pdf
import os

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("📄 Створити заяву"), KeyboardButton("ℹ️ Про бота"))

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Вітаємо в ЮрБоті! Створюйте юридичні заяви українською мовою.\n\nНатисніть: 📄 Створити заяву",
        reply_markup=main_kb
    )

@dp.message_handler(lambda msg: msg.text == "ℹ️ Про бота")
async def about(message: types.Message):
    await message.answer("🧾 Цей бот допомагає сформувати офіційні заяви у PDF. Станьте юридично захищеним — швидко та зручно.")

@dp.message_handler(lambda msg: msg.text == "📄 Створити заяву")
async def choose_type(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("ОСББ"), KeyboardButton("ЦНАП"), KeyboardButton("Поліція"))
    kb.add(KeyboardButton("⬅️ Назад"))
    await message.answer("Оберіть тип заяви:", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text in ["ОСББ", "ЦНАП", "Поліція"])
async def get_data(message: types.Message):
    await message.answer("✍️ Введіть своє ПІБ:")
    dp.register_message_handler(get_name, state=message.text)

user_data = {}

async def get_name(message: types.Message):
    user_data[message.from_user.id] = {"name": message.text}
    await message.answer("📍 Введіть вашу адресу:")

    dp.register_message_handler(get_address, state="address")

async def get_address(message: types.Message):
    user_data[message.from_user.id]["address"] = message.text
    await message.answer("📝 Опишіть проблему коротко:")

    dp.register_message_handler(generate_zayava, state="problem")

async def generate_zayava(message: types.Message):
    user_data[message.from_user.id]["problem"] = message.text

    # PDF генерація
    uid = message.from_user.id
    name = user_data[uid]["name"]
    address = user_data[uid]["address"]
    problem = user_data[uid]["problem"]

    pdf_path = generate_pdf(name, address, problem)

    with open(pdf_path, "rb") as doc:
        await message.answer_document(doc, caption="✅ Ось ваша згенерована заява (чернетка).")

    os.remove(pdf_path)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

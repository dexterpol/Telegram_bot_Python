import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from manipulador import process_materials 
from PyPDF2 import PdfReader


logging.basicConfig(level=logging.INFO)

API_TOKEN = '6449763875:AAFu17HiSDSn-CKWu6cvrtsZcHcm8si1ED0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_document(message: types.Message):
    try:
        print("Received a document")
        document = message.document
        file_path = await bot.download_file_by_id(document.file_id)
        print("Document ID:", document.file_id)
        await process_materials(file_path, message.chat.id, bot)
        await message.reply("Documento recebido e processado com sucesso!")
    except Exception as e:
        await message.reply(f"Ocorreu um erro ao processar o documento: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
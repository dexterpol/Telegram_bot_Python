from aiogram import Bot
from aiogram.types import InputFile
import os

async def process_materials(file_id, chat_id, bot):
    try:
        # Get file object using the file_id
        file_obj = await bot.get_file(file_id)
        file_path = file_obj.file_path

        # Download the file
        downloaded_file = await bot.download_file(file_path)

        # Process and send materials
        with open(downloaded_file, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                material = line.strip()
                await send_material(chat_id, material, bot)
        
        # Delete the downloaded file
        os.remove(downloaded_file)

    except Exception as e:
        print(f"Erro ao processar materiais: {e}")

async def send_material(chat_id, material, bot):
    try:
        await bot.send_message(chat_id, f"Material: {material}")
    except Exception as e:
        print(f"Erro ao enviar material: {e}")

import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from PyPDF2 import PdfReader
from openpyxl import Workbook


logging.basicConfig(level=logging.INFO)

API_TOKEN = '6449763875:AAFu17HiSDSn-CKWu6cvrtsZcHcm8si1ED0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Estrutura para armazenar temporariamente as informações do usuário
class UserState(StatesGroup):
    espera_dados = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Envie os dados no formato: data descricao valor")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_text(message: types.Message, state: FSMContext):
    data = {}
    async with state.proxy() as _data:
        _data.update(data)
        text = message.text
        
        # Separe as entradas com base em quebra de linha
        entries = text.split('\n')
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Data", "Descrição", "Valor"])  # Cabeçalho da planilha

        # Processar cada entrada e adicioná-la à planilha
        for entry in entries:
            # Extrair informações usando expressões regulares
            pattern = r'(\d{2}/\d{2}\s(.*?)\s([\d,]+))'
            matches = re.findall(pattern, entry)

            if matches:
                for match in matches:
                    data['data'] = f'{match[0]}/{match[1]}'
                    data['descricao'] = match[1]
                    data['valor'] = match[2]

                    # Adicionar os dados à planilha
                    sheet.append([data['data'][0:2], data['descricao'], data['valor']])

        # Salvar a planilha
        workbook.save("dados.xlsx")

        # Enviar o Excel para o usuário do Telegram
        await message.reply_document(open('dados.xlsx', 'rb'))

        # Finalizar o estado da conversa
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import aiogram
import asyncio
import logging
from aiogram import Dispatcher, Router, types, Bot
from aiogram.filters import CommandStart, Command
import keyboards
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
import keyboards
from callbacks import router as call_router



bot = Bot(token='7577362956:AAEQzx0qXLKCcvVA5PNj50ot7OeT6Dai0eY')
dp = Dispatcher(storage=MemoryStorage())
router = Router()
router.include_router(call_router)


@router.message(CommandStart())
async def welcome(m: types.Message):
    await m.answer(
        text='Привет, ты находишься в боте для создания чеков. Выбери нужный бренд из списка ниже:',
        reply_markup=keyboards.get_brand_kb(1)
    )


@router.message(Command('get'))
async def g (m: types.Message):
    await m.answer(
        text=f'{m.chat.id}'
    )

async def main():
    logger = logging.getLogger('aiogram')
    logger.setLevel(logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
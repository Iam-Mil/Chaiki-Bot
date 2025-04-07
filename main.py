import asyncio
import logging
from aiogram import Router, types, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from keyboards import get_brand_kb
from aiogram.fsm.storage.memory import MemoryStorage
from callbacks import router as call_router

router = Router()
router.include_router(call_router)


@router.message(CommandStart())
async def welcome(m: types.Message):
    await m.answer(
        text='Привет, ты находишься в боте для создания чеков. Выбери нужный бренд из списка ниже:',
        reply_markup=get_brand_kb(1)
    )


@router.message(Command('get'))
async def g(m: types.Message):
    await m.answer(
        text=f'{m.chat.id}'
    )


async def main():
    logger = logging.getLogger('aiogram')
    logger.setLevel(logging.INFO)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    bot = Bot(token='7577362956:AAEQzx0qXLKCcvVA5PNj50ot7OeT6Dai0eY')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
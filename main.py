import asyncio
import logging
from aiogram import Router, types, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router as call_router

router = Router()
router.include_router(call_router)

async def main():
    logger = logging.getLogger('aiogram')
    logger.setLevel(logging.INFO)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    bot = Bot(token='7577362956:AAEQzx0qXLKCcvVA5PNj50ot7OeT6Dai0eY')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
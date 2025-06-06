from env import BOT_TOKEN

import asyncio
import logging
from aiogram import Router, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router as call_router

router = Router()
router.include_router(call_router)


async def main():
    logger = logging.getLogger('aiogram')
    logger.setLevel(logging.INFO)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    bot = Bot(token=BOT_TOKEN)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
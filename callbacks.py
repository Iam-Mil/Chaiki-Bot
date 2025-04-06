from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
import keyboards
from aiogram.exceptions import TelegramBadRequest

router = Router()


@router.callback_query(F.data.startswith('page_'))
async def change_kb(callback: CallbackQuery):
    num = int(callback.data.replace('page_', ''))
    try:
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.get_brand_kb(num)
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data.startswith('brand_'))
async def input_brand(callback: CallbackQuery):
    brand = callback.data.replace('brand_', '').capitalize()
    await callback.message.answer(
        text=f'Вы выбрали {brand}'
    )
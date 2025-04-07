from aiogram import Router, Bot, types
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

from form import Forms

import keyboards
from aiogram.exceptions import TelegramBadRequest

router = Router()


@router.message(CommandStart())
async def welcome(message_or_callback: types.Message | types.CallbackQuery, bot: Bot):
    await bot.send_message(message_or_callback.from_user.id,
                           text='Привет, ты находишься в боте для создания чеков. Выбери нужный бренд из списка ниже:',
                           reply_markup=keyboards.get_brand_kb(1)
                           )


@router.message(Command('get'))
async def g(m: types.Message):
    await m.answer(
        text=f'{m.chat.id}'
    )


# Смена страницы при выборе брендов
@router.callback_query(F.data.startswith('page_'))
async def change_kb(callback: CallbackQuery):
    num = int(callback.data.replace('page_', ''))
    try:
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.get_brand_kb(num)
        )
    except TelegramBadRequest:
        pass


# Ввод бренда
@router.callback_query(F.data.startswith('brand_'))
async def input_brand(callback: CallbackQuery, bot: Bot, state: FSMContext):
    brand = callback.data.replace('brand_', '')

    await state.update_data({'brand': brand})

    await callback.message.answer(
        text=f'Вы выбрали {brand.capitalize().replace('_', ' ')}'
    )


@router.callback_query(F.data.startswith('from_brand_continue'))
async def from_brand_continue(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()

    form = Forms.get_by_name(data.get('brand'))
    await state.update_data({'input_form': form})

    if not form:
        await bot.send_message(callback.from_user.id, 'Нет формы')
        return

    first_field = form.fields[0]

    await state.set_state(first_field.state)
    await bot.send_message(callback.from_user.id, first_field.message, reply_markup=keyboards.back_kb())


@router.callback_query(F.data == 'back', StateFilter(*Forms.get_all_states()))
async def back_form_input(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    full_state_name = await state.get_state()
    state_name = full_state_name.split(':')[-1]

    data = await state.get_data()
    form = data.get('input_form')

    current_state = getattr(form.states, state_name)
    current_field = form.get_field_by_state(current_state)

    prev_field = form.get_prev_field(current_field)

    if prev_field:
        await state.set_state(prev_field.state)
        await bot.send_message(callback.from_user.id, prev_field.message, reply_markup=keyboards.back_kb())
    else:
        await welcome(callback, bot)


@router.message(StateFilter(*Forms.get_all_states()))
async def get_form_input(message: types.Message, bot: Bot, state: FSMContext):
    full_state_name = await state.get_state()
    state_name = full_state_name.split(':')[-1]

    value = message.text

    data = await state.get_data()
    form = data.get('input_form')

    current_state = getattr(form.states, state_name)
    current_field = form.get_field_by_state(current_state)

    proceed = False

    if current_field.validators:
        for validator in current_field.validators:
            result = validator(value)
            if result['status']:
                proceed = True
            else:
                await bot.send_message(message.from_user.id, result['error'])
                await bot.send_message(message.from_user.id, current_field.message)
                proceed = False
                break

    if proceed:
        await state.update_data({f'input_form_{current_field.name}': value})

        next_field = form.get_next_field(current_field)

        if next_field:
            await state.set_state(next_field.state)
            await bot.send_message(message.from_user.id, next_field.message, reply_markup=keyboards.back_kb())
        else:
            data = await state.get_data()

            summary = f'brand: {data.get("brand")}\n'

            for key in data:
                if key.startswith('input_form_'):
                    summary += f'{key.replace("input_form_", "")}: {data[key]}\n'

            await bot.send_message(message.from_user.id, summary)
            await welcome(message, bot)

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.models.main import VKGroup
from bot.tg_bot.states import EventStates


async def bot_start_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply('Обновлено!')


async def bot_add_group_command(message: types.Message, state: FSMContext):
    await EventStates.event_add_new_group.set()
    await message.reply('Написать логин группы')


async def bot_add_group_name_message(message: types.Message, state: FSMContext):
    login = message.text.strip()
    await VKGroup.get_or_create(name=login)
    await state.reset_state()
    await message.reply(f'login: {login}')

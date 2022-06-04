import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor

from bot.models.main import Post
from bot.tg_bot.handlers import bot_start_command, bot_add_group_command, bot_add_group_name_message
from bot.tg_bot.states import EventStates


async def on_start_up():
    print('started')


class TGBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.admin_channel = os.environ.get('admin_channel')

    async def register_handles(self):
        dp = self.dp
        dp.register_message_handler(bot_start_command, CommandStart(), state='*')
        dp.register_message_handler(bot_add_group_command, commands=['add'], state='*')
        dp.register_message_handler(bot_add_group_name_message, lambda message: message,
                                    state=EventStates.event_add_new_group)

        # aioschedule

    async def send_post(self, post: Post):
        channel_id = f'@{self.admin_channel}'
        if post.photo == "":
            await self.bot.send_message(channel_id, post.text, parse_mode='HTML')
        else:
            try:
                await self.bot.send_photo(channel_id, photo=post.photo, caption=post.text, parse_mode='HTML')
            except Exception as e:
                print(e)
                await self.bot.send_message(channel_id, post.text, parse_mode='HTML')

        post.is_sent = True
        await post.save(update_fields=['is_sent'])

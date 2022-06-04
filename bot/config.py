import os
from dataclasses import dataclass

from bot.models.main import db_init
from dotenv import find_dotenv, load_dotenv


@dataclass
class Config:
    vk_token: str
    tg_token: str


async def load_config():
    load_dotenv(find_dotenv())

    await db_init()

    tg_bot_token = os.environ.get('TG')
    vk_bot_token = os.environ.get('VK')

    return Config(vk_token=vk_bot_token, tg_token=tg_bot_token)

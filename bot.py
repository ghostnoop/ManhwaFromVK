import asyncio

import aioschedule
from aiogram.utils import executor

from bot.config import load_config
from bot.tg_bot.tg_bot import TGBot, on_start_up
from bot.vk_bot.vk_bot import VKBot
from bot.models.main import Post, VKGroup, db_init


async def on_start_up(*args):
    await db_init()
    await tg.register_handles()


def start_bots():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_start())
    # await tg.start()
    print('started')
    executor.start_polling(tg.dp, on_startup=on_start_up, loop=loop, skip_updates=True)


async def scheduler_job():
    try:
        async for posts in vk.get_posts_from_groups():
            for post in posts:
                await tg.send_post(post)
    except Exception as e:
        print(e)


async def scheduler_start():
    await db_init()
    await scheduler_job()
    aioschedule.every(10).minutes.do(scheduler_job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    config = load_config()
    vk = VKBot(config.vk_token)
    tg = TGBot(config.tg_token)
    start_bots()

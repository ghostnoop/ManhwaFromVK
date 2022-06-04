import asyncio

from aiogram import Bot


async def test():
    bot = Bot(token='10sadyoYUI')
    url = 'https://m.vk.com/@lnmanga-vechnyi-pervyi-bog-120-glava'
    await bot.send_photo('@mandlyme', photo=url)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())

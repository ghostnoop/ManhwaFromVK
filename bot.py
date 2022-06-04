from bot.config import load_config
from bot.vk_bot.vk_bot import VKBot
from bot.models.main import Post, VKGroup


async def worker():
    config = await load_config()
    vk = VKBot(config.vk_token)


async def get_posts_from_groups(vk: VKBot):
    groups = await VKGroup.all()
    for group in groups:
        await vk.get_posts(group)


import asyncio
import os
from datetime import datetime

from vkwave.api import API, BotSyncSingleToken, Token
from vkwave.api.token.token import UserSyncSingleToken

from bot.models.main import Post, VKGroup


class VKBot:
    def __init__(self, token: str):
        self.__token = Token(token)
        api_session = API(tokens=UserSyncSingleToken(self.__token))
        self.api = api_session.get_context()

    # async def bot_init(self):
    #     posts = await api.wall.get(domain='lnmanga')
    #     print(posts)

    async def get_posts(self, vk_group: VKGroup):
        posts = await self.api.wall.get(domain=vk_group.name)
        last_exist_post = await Post.filter(group=vk_group).order_by('-id').limit(1).first()
        if last_exist_post is None:
            last_exist_post = -1
        else:
            last_exist_post = last_exist_post.created_at
            last_exist_post = int(last_exist_post.timestamp())

        new_posts = []
        for post in posts:
            created_at = post.date
            if created_at > last_exist_post:
                new_posts.append(Post(post_id=post.id,
                                      group=vk_group,
                                      text=post.text,
                                      photo='',
                                      created_at=datetime.fromtimestamp(created_at)
                                      ))
        return new_posts


if __name__ == '__main__':
    import os
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())

    token = os.environ.get('VK')


    async def test():
        vk = VKBot(token)
        await vk.bot_init()


    asyncio.get_event_loop().run_until_complete(test())

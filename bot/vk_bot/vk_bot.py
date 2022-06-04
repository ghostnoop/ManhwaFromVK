import asyncio
import os

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
        posts = await self.api.wall.get(domain=vk_group.name, count=100)
        last_exist_post = vk_group.newest_created_at_post
        if last_exist_post is None:
            last_exist_post = -1

        new_posts = []
        max_created_at = -1
        posts = posts.response.items
        for post in posts:
            created_at = post.date
            if created_at > max_created_at:
                max_created_at = created_at

            if created_at > last_exist_post:
                if len(post.attachments) > 0:
                    attachment = post.attachments[0]
                    link = attachment.link
                    url = link.url
                    title = link.title
                    text = f'{title}\n\n{post.text}'
                else:
                    text = post.text
                    url = ""

                new_posts.append(Post(post_id=post.id,
                                      group=vk_group,
                                      text=text,
                                      photo=url,
                                      created_at=created_at
                                      ))
        return new_posts, max_created_at

    async def get_posts_from_groups(self):
        groups = await VKGroup.all()
        for group in groups:
            posts, max_created_at = await self.get_posts(group)
            yield posts
            group.newest_created_at_post = max_created_at
            print(group.name, 'date', group.newest_created_at_post)
            await group.save(update_fields=['newest_created_at_post'])


if __name__ == '__main__':
    import os
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())

    token = os.environ.get('VK')


    async def test():
        vk = VKBot(token)
        await vk.bot_init()


    asyncio.get_event_loop().run_until_complete(test())

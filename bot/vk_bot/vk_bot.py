from vkwave.api import API, BotSyncSingleToken, Token


class VKBot:
    def __init__(self, token: str):
        self.token = BotSyncSingleToken(Token(token))

    async def bot_init(self):
        async with API(tokens=self.token) as api:
            api_ctx = api.get_context()
            get_user = (await api_ctx.users.get(user_ids=1)).response[0].first_name
            await api_ctx.api_options.clients[0].close()
            print(get_user)

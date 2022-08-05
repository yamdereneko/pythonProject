import asyncio
import botpy
from botpy.message import Message
from botpy.message import DirectMessage


class MyClient(botpy.Client):
    async def on_message_create(self, message: Message):
        member = await self.api.get_guild_member(guild_id=message.guild_id, user_id=message.author.id)
        botpy.logger.info(f'member: {member}')
        botpy.logger.info(f'message: {message}')
        if message.content == "11":
            botpy.logger.info(f'message {"yes"}')
            await self.api.post_message(channel_id=message.channel_id, content="好家伙")


intents = botpy.Intents(direct_message=True, guilds=True, guild_messages=True)
client = MyClient(intents=intents)
client.run(appid="102019860", token="iDizSgjWJr6Dbx6DJcEXHvheudRWrdVg")

from valorantcompetitivebot.discordbot.client import DiscordClient
from valorantcompetitivebot.config.config import DiscordConfig


async def start(config: DiscordConfig):
    instance = DiscordClient()
    await instance.start(config.token)

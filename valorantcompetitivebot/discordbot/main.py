from valorantcompetitivebot.config.config import DiscordConfig
from valorantcompetitivebot.discordbot.client import DiscordClient
from valorantcompetitivebot.reddit.reddit import Reddit


async def start(config: DiscordConfig, reddit: Reddit):
    instance = DiscordClient(reddit, config)
    await instance.start(config.token)

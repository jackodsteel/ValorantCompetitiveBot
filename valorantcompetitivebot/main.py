import asyncio

import valorantcompetitivebot.discordbot.main as discord
import valorantcompetitivebot.webserver.main as webserver
from valorantcompetitivebot.config.config import BotConfig, RedditConfig
from valorantcompetitivebot.reddit.reddit import Reddit


# TODO(jsteel): Make the filepath configurable
def load_config() -> BotConfig:
    return BotConfig.parse_from_file("config/config.yaml")


def load_reddit(config: RedditConfig) -> Reddit:
    return Reddit(config)


def register_tasks(loop: asyncio.AbstractEventLoop, config: BotConfig, reddit: Reddit):
    """All new tasks should be added here."""
    loop.create_task(webserver.start())
    loop.create_task(discord.start(config.discord_config, reddit))


if __name__ == '__main__':
    _config = load_config()
    _reddit = load_reddit(_config.reddit_config)

    _loop = asyncio.get_event_loop()
    register_tasks(_loop, _config, _reddit)
    _loop.run_forever()
    _loop.close()

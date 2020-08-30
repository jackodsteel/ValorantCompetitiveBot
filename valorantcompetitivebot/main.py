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


def main():
    config = load_config()
    reddit = load_reddit(config.reddit_config)
    loop = asyncio.get_event_loop()
    try:
        register_tasks(loop, config, reddit)
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    main()

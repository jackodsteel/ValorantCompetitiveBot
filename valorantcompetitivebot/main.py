import asyncio

import valorantcompetitivebot.webserver.main as webserver
import valorantcompetitivebot.discordbot.main as discord
from valorantcompetitivebot.config.config import BotConfig


# TODO(jsteel): Make the filepath configurable
def load_config() -> BotConfig:
    return BotConfig.parse_from_file("config/config.yaml")


def register_tasks(config: BotConfig):
    """All new tasks should be added here."""
    loop.create_task(webserver.start())
    loop.create_task(discord.start(config.discord_config))


if __name__ == '__main__':
    _config = load_config()

    loop = asyncio.get_event_loop()
    register_tasks(_config)
    loop.run_forever()
    loop.close()

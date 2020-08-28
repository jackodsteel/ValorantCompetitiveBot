import asyncio

import valorantcompetitivebot.webserver.main as webserver
import valorantcompetitivebot.discord2.main as discord


def register_tasks():
    """All new tasks should be added here."""
    loop.create_task(webserver.start())
    loop.create_task(discord.start())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    register_tasks()
    loop.run_forever()
    loop.close()

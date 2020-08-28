import asyncio
import valorantcompetitivebot.webserver.main as webserver

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(webserver.main())
    loop.run_forever()
    loop.close()

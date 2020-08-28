# Important decisions

## Language

Python 3 has been selected as the language of choice as it is the most common language used by other Reddit developers.

## Framework

Since we're building from the ground up, using asyncio seems like a good choice.

Since we're using asyncio, aiohttp seems like a natural choice to best handle the web server.

## Storage

TODO(jsteel): Decide this.

ORM? Tie to a cloud provider?

For now just start with a storage dir and use SQLite I think
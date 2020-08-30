import discord
import discord.ext.commands as commands

from valorantcompetitivebot.config.config import DiscordConfig
from valorantcompetitivebot.error.errors import BotError
from valorantcompetitivebot.reddit.reddit import Reddit


class DiscordClient(commands.Bot):
    def __init__(self, reddit: Reddit, config: DiscordConfig):
        # TODO(jsteel): Make command_prefix alterable?
        super().__init__(command_prefix="!")
        self.add_cog(BotCog(reddit, config))


class BotCog(commands.Cog):
    def __init__(self, reddit: Reddit, config: DiscordConfig):
        self._reddit = reddit
        self._config = config
        self._allowed_roles = set(config.allowed_roles)

    @commands.Cog.listener()
    async def on_command_error(self, _, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error

    @commands.command()
    async def sticky(self, context: commands.Context, *args: str):
        try:
            post_url = self.get_url(*args)
            self.validate_permissions(context.author)
            await self._reddit.sticky_post(post_url)
        except BotError as e:
            return await context.send(e.user_message)
        return await context.send("Done :)")

    @commands.command()
    async def unsticky(self, context: commands.Context, *args: str):
        try:
            post_url = self.get_url(*args)
            self.validate_permissions(context.author)
            await self._reddit.unsticky_post(post_url)
        except BotError as e:
            return await context.send(e.user_message)
        return await context.send("Done :)")

    @staticmethod
    def get_url(*args: str) -> str:
        if len(args) == 0:
            raise DiscordError("Must provide a link!")
        if len(args) > 1:
            raise DiscordError("Just a single link please!")
        return args[0]

    def validate_permissions(self, author: discord.Member):
        role_names = map(lambda role: role.name, author.roles)
        if self._allowed_roles.isdisjoint(role_names):
            raise DiscordError("You don't have permission to do that!")


class DiscordError(BotError):
    pass

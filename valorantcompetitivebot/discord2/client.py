# import discord
#
#
# class DiscordClient(discord.Client):
#     async def on_message(self, message):
#         if message.author == self.user:
#             return
#
#         if message.content.startswith('$hello'):
#             await message.channel.send('Hello World!')

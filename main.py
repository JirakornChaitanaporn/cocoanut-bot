import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()

class CocoanutBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix="$", intents=intents, help_command=None)

    async def setup_hook(self):
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.debug")

    async def on_ready(self):
        print("ready")


bot = CocoanutBot()
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
bot.run(os.getenv("DISCORD_TOKEN"), log_handler=handler, log_level=logging.DEBUG)

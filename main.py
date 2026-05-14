import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename="discord.log",encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("ready")

@bot.command(name="help")
async def help(ctx):
    print("help")
    embed = discord.Embed(
        title="Bot Command Menu",
        description="Here is a list of everything I can do!",
        color=discord.Color.blue()
    )

    # Add sections for your commands
    embed.add_field(name="Help", value="`$help` - Use this to see list of command", inline=False)
    
    embed.add_field(name="Translate Korean", value="`$koreanT` - when use this command upload a korean manga picture with it to get translate\nNote: one page only", inline=False)

    embed.add_field(name="Check Token", value="`$checkToken` - Use this to see how many image left can you upload this month", inline=False)
    # AWAIT the send because we are waiting for Discord to receive the embed!
    await ctx.send(embed=embed)
    
@bot.command(name="DEBUG_read_image")
async def check_read_image(ctx):
    # Check if there is at least one attachment
    if ctx.message.attachments:
        # Get the first attachment in the list
        image_url = ctx.message.attachments[0].url
        await ctx.send(f"I see your image! Here is the link: {image_url}")
    else:
        await ctx.send("You didn't attach an image!")
        
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
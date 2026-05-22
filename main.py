import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from ocr import KoreanOcr
import cv2

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
    # 1. Check if any attachment exists
    if not ctx.message.attachments:
        return await ctx.send("You didn't attach anything!")

    # 2. Get the first attachment
    attachment = ctx.message.attachments[0]
    
    # 3. Define allowed extensions
    valid_extensions = ('.png', '.jpeg', '.jpg')

    # 4. Validate the filename
    if attachment.filename.lower().endswith(valid_extensions):
        image_url = attachment.url
        await ctx.send(f"Valid image detected! Link: {image_url}")
    else:
        await ctx.send("That's not a valid image file (.png, .jpg, or .jpeg only)!")
        
@bot.command(name="DEBUG_read_image_text")
async def check_read_image_text(ctx):
    # 1. Check if any attachment exists
    if not ctx.message.attachments:
        return await ctx.send("You didn't attach anything!")

    # 2. Get the first attachment
    attachment = ctx.message.attachments[0]
    
    # 3. Define allowed extensions
    valid_extensions = ('.png', '.jpeg', '.jpg', '.webp')

    # 4. Validate the filename
    if attachment.filename.lower().endswith(valid_extensions):
        image_url = attachment.url
        #call korean ocr
        read_text = KoreanOcr.get_instance().make_text(image_url)
        await ctx.send(f"{ctx.author.mention}\n{read_text}")
    else:
        await ctx.send("That's not a valid image file (.png, .jpg, or .jpeg only)!")
        
        
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
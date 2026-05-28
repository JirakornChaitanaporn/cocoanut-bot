import discord
from discord.ext import commands
from cores.ocr import KoreanOcr


class Debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="DEBUG_help")
    async def debug_help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Bot Command Menu",
            description="Here is a list of everything I can do!",
            color=discord.Color.blue()
        )
        embed.add_field(name="read image", value="`$DEBUG_read_image` - this command is use for checking image validation", inline=False)
        embed.add_field(name="read text image", value="`$DEBUG_read_image_text` - Use this to to read all korean text in the image", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="DEBUG_read_image")
    async def check_read_image(self, ctx: commands.Context):
        if not ctx.message.attachments:
            return await ctx.send("You didn't attach anything!")

        attachment = ctx.message.attachments[0]
        valid_extensions = ('.png', '.jpeg', '.jpg')

        if attachment.filename.lower().endswith(valid_extensions):
            await ctx.send(f"{ctx.author.mention}\nValid image detected! Link: {attachment.url}")
        else:
            await ctx.send(f"{ctx.author.mention}\nThat's not a valid image file (.png, .jpg, or .jpeg only)!")

    @commands.command(name="DEBUG_read_image_text")
    async def check_read_image_text(self, ctx: commands.Context):
        if not ctx.message.attachments:
            return await ctx.send(f"{ctx.author.mention}\nYou didn't attach anything!")

        valid_extensions = ('.png', '.jpeg', '.jpg', '.webp')
        response_lines = [f"{ctx.author.mention} **OCR Results Summary:**\n"]
        processed_any = False

        for index, attachment in enumerate(ctx.message.attachments, start=1):
            if attachment.filename.lower().endswith(valid_extensions):
                processed_any = True
                read_text = KoreanOcr.get_instance().make_text(attachment.url)
                response_lines.append(f"**Image #{index}:**\n{read_text}\n")
            else:
                response_lines.append(f"⚠️ Skipped `{attachment.filename}` (Invalid format)\n")

        if not processed_any:
            return await ctx.send(f"{ctx.author.mention}\nNone of the attached files were valid images (.png, .jpg, .jpeg, .webp)!")

        await ctx.send("\n".join(response_lines))


async def setup(bot: commands.Bot):
    await bot.add_cog(Debug(bot))

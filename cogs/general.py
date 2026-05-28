import discord
from discord.ext import commands
from cores.ocr import KoreanOcr


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Bot Command Menu",
            description="Here is a list of everything I can do!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Help", value="`$help` - Use this to see list of command", inline=False)
        embed.add_field(name="Translate Korean", value="`$translate_manhwa` - when use this command upload a korean manga picture with it to get translate\nNote: one page only", inline=False)
        embed.add_field(name="Check limit", value="`$check_limit` - Use this to see how many image left can you upload this month", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="check_limit")
    async def check_limit(self, ctx: commands.Context):
        pass

    @commands.command(name="translate_manhwa")
    async def translate_manhwa(self, ctx: commands.Context):
        if not ctx.message.attachments:
            return await ctx.send(f"{ctx.author.mention}\nYou didn't attach anything!")

        attachment = ctx.message.attachments[0]
        valid_extensions = ('.png', '.jpeg', '.jpg', '.webp')

        if attachment.filename.lower().endswith(valid_extensions):
            image_url = attachment.url
            read_text = KoreanOcr.get_instance().make_text(image_url)
            await ctx.send(f"{ctx.author.mention}\n{read_text}")
        else:
            await ctx.send(f"{ctx.author.mention}\nThat's not a valid image file (.png, .jpg, or .jpeg only)!")


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))

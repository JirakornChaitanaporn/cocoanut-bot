import discord
from discord.ext import commands
from cores.ocr import KoreanOcr
from cores.transalate_api import Translator_api

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
        
        if len(ctx.message.attachments) > 5:
            return await ctx.send(f"{ctx.author.mention}\nYou can only upload 5 image at a time sorry for inconvience")

        valid_extensions = ('.png', '.jpeg', '.jpg', '.webp')
        response_lines = [f"**OCR Results Summary:**\n"]
        processed_any = False

        for index, attachment in enumerate(ctx.message.attachments, start=1):
            if attachment.filename.lower().endswith(valid_extensions):
                processed_any = True
                read_text = KoreanOcr.get_instance().make_text(attachment.url)
                response_lines.append(f"**Image #{index}:**\n{read_text}\n")
            else:
                response_lines.append(f"⚠️ **Image #{index} Skipped `{attachment.filename}` (Invalid format)\n")

        if not processed_any:
            return await ctx.send(f"{ctx.author.mention}\nNone of the attached files were valid images (.png, .jpg, .jpeg, .webp)!")

        ocr_result = "\n".join(response_lines)
        translated = f"{ctx.author.mention}\n{Translator_api.get_instance().translate(ocr_result)}"
  
        return await ctx.send(translated)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))

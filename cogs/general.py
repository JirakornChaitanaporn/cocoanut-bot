import discord
from discord.ext import commands
from cores.ocr import KoreanOcr
from cores.transalate_api import Translator_api
from cores.daily_quota import DailyQuota, DAILY_IMAGE_LIMIT

class General(commands.Cog):
    genders = ("non_binary",
                "genderqueer",
                "genderfluid",
                "agender",
                "bigender",
                "pangender",
                "two_spirit",
                "demiboy",
                "demigirl",
                "gay",
                "lesbian",
                "bisexual",
                "queer",
                "tomboy",)

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.quota = DailyQuota()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content.strip()
        command_text = content[1:].lower()
        if content.startswith("$") and any(keyword in command_text for keyword in self.genders):
            await message.channel.send(f"{message.author.mention} hey please respect people in all gender!")

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Bot Command Menu",
            description="Here is a list of everything I can do!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Help", value="`$help` - Use this to see list of command", inline=False)
        embed.add_field(name="Translate Korean", value="`$translate_manhwa` - Attach up to 5 Korean manga images to translate. Limit: 80 images per user per day.", inline=False)
        embed.add_field(name="Check limit", value="`$check_limit` - See today's remaining images. Resets at 00:00 Thailand time (GMT+7).", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="check_limit")
    async def check_limit(self, ctx: commands.Context):
        remaining = self.quota.remaining(ctx.author.id)
        await ctx.send(
            f"{ctx.author.mention}\nYou have {remaining}/{DAILY_IMAGE_LIMIT} images left today. "
            "Your allowance resets at 00:00 Thailand time (GMT+7)."
        )

    @commands.command(name="translate_manhwa")
    async def translate_manhwa(self, ctx: commands.Context):
        if not ctx.message.attachments:
            return await ctx.send(f"{ctx.author.mention}\nYou didn't attach anything!")
        
        if len(ctx.message.attachments) > 5:
            return await ctx.send(f"{ctx.author.mention}\nYou can only upload 5 image at a time sorry for inconvience")

        valid_extensions = ('.png', '.jpeg', '.jpg', '.webp')
        image_count = sum(
            attachment.filename.lower().endswith(valid_extensions)
            for attachment in ctx.message.attachments
        )
        if not image_count:
            return await ctx.send(f"{ctx.author.mention}\nNone of the attached files were valid images (.png, .jpg, .jpeg, .webp)!")
        accepted, remaining = self.quota.reserve(ctx.author.id, image_count)
        if not accepted:
            return await ctx.send(
                f"{ctx.author.mention}\nYou have {remaining}/{DAILY_IMAGE_LIMIT} images left today, "
                f"but this request contains {image_count} images. No images were processed. "
                "Upload fewer images or wait until 00:00 Thailand time (GMT+7)."
            )
        response_lines = [f"**OCR Results Summary:**\n"]
        processed_any = False

        for index, attachment in enumerate(ctx.message.attachments, start=1):
            if attachment.filename.lower().endswith(valid_extensions):
                processed_any = True
                read_text = KoreanOcr().make_text(attachment.url)
                response_lines.append(f"**Image #{index}:**\n{read_text}\n")
            else:
                response_lines.append(f"⚠️ **Image #{index} Skipped `{attachment.filename}` (Invalid format)\n")

        if not processed_any:
            return await ctx.send(f"{ctx.author.mention}\nNone of the attached files were valid images (.png, .jpg, .jpeg, .webp)!")

        ocr_result = "\n".join(response_lines)
        translated = f"{ctx.author.mention}\n{Translator_api().translate(ocr_result)}"
  
        return await ctx.send(translated)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))

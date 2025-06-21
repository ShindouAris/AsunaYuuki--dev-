from disnake.ext import commands
from disnake import ApplicationCommandInteraction, MessageCommandInteraction
from utils.ClientUser import ClientUser
import disnake
from typing import Union
class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot: ClientUser = bot

    @commands.command(name="purge", description="Xóa tin nhắn trong kênh")
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge_legacy(self, ctx: disnake.AppCommandInteraction, amount: int = None):
        await ctx.message.delete()
        await self.purge.callback(self=self, ctx=ctx, amount=amount)

    @commands.slash_command(name="purge", description=f"Xóa tin nhắn trong kênh",
                            options=[disnake.Option(name="amount",
                                                    description="Số lượng tin nhắn cần xóa",
                                                    type=disnake.OptionType.integer,
                                                    required=True
                                                    )])
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def purge(self, ctx: ApplicationCommandInteraction, amount: int = None):
        if ctx.author.bot:
            return

        await ctx.response.defer()

        if amount is None:
            await ctx.send("Vui lòng nhập số lượng tin nhắn cần xóa.")
            return

        if 0 >= amount > 100:
            await ctx.send("Số lượng không hợp lệ, vui lòng nhập số lượng từ 1 đến 100.")
            return

        deleted = await ctx.channel.purge(limit=amount)
        try:
            await ctx.edit_original_response(embed=disnake.Embed(title=f"♻️ Đã xóa {len(deleted)} tin nhắn", color=disnake.Color.green()))
        except AttributeError:
            await ctx.send(embed=disnake.Embed(title=f"♻️ Đã xóa {len(deleted)} tin nhắn", color=disnake.Color.green()), delete_after=5)

def setup(bot):
    bot.add_cog(Purge(bot))

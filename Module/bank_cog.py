# bank_cog.py
from utils.ClientUser import ClientUser
import disnake
from disnake.ext import commands

class Bank(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot: ClientUser = bot
        self.accounts = {
                "ngan_hang": "MB Bank <:emoji_48:1382077487609282720>",
                "so_tai_khoan": "9990328421004",
                "chu_tai_khoan": "NGUYEN ANH NHAT",
                "qr_data": "https://cdn.discordapp.com/attachments/1370732207177596989/1385459230085222592/IMG_20250620_101524.jpg?ex=685624f5&is=6854d375&hm=8ac93d4ebd77c6816d8aee6074b270786f2d7cad22e6cabebca23c0083cd8047&"
            }
        

    def create_embed(self) -> disnake.Embed:
        # Dùng embed chung, thumbnail là QR đầu tiên
        embed = disnake.Embed(
            title="📋 Danh sách tài khoản chuyển khoản",
            color=disnake.Color.green()
        )
        # Thumbnail sẽ hiển thị QR của account đầu
        first_qr = self.accounts["qr_data"]
        embed.set_thumbnail(url=first_qr)

        
        name = f"{self.accounts.get('ngan_hang')} • {self.accounts.get('chu_tai_khoan')}"
        value = f"Số TK: `{self.accounts.get('so_tai_khoan')}`\n" \
                f"[Xem QR chuyển khoản]({self.accounts.get('qr_data')})"
        embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="Nhập sai quá 3 lần sẽ từ chối nhận thẻ…")
        return embed

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="bank", description="Hiện danh sách bank")
    async def message_bank(self, ctx: commands.Context):
        if ctx.author.bot:
            return
        embed = self.create_embed()
        await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="bank", description="Hiện danh sách bank")
    async def slash_bank(self, inter: disnake.ApplicationCommandInteraction):
        if inter.author.bot:
            return
        try:
            await inter.response.defer(ephemeral=True)
        except:
            pass
        embed = self.create_embed()
        await inter.followup.send(embed=embed, ephemeral=True)

def setup(bot: ClientUser):
    bot.add_cog(Bank(bot))


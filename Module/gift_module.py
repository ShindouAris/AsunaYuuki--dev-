import disnake as discord
from disnake import app_commands
from disnake.ext import commands

class GiftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Đăng ký slash command
        self.bot.tree.add_command(self.givegift)

    @app_commands.command(
        name="givegift",
        description="Tặng quà cho một thành viên"
    )
    @app_commands.describe(
        user="Thành viên bạn muốn tặng quà",
        gift="Tên món quà (ví dụ: hoa, chocolate, voucher ...)",
        message="Lời nhắn kèm (không bắt buộc)"
    )
    async def givegift(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        gift: str,
        message: str = None
    ):
        # Tạo embed quà tặng
        embed = discord.Embed(
            title="🎁 Bạn nhận được quà!",
            description=f"{interaction.user.mention} đã tặng bạn **{gift}**!",
            color=discord.Color.random()
        )
        if message:
            embed.add_field(name="💌 Lời nhắn", value=message, inline=False)
        embed.set_footer(text=f"Tặng quà bởi {interaction.user.display_name}")
        
        # Gửi embed vào kênh hiện tại và DM riêng cho người nhận
        await interaction.response.send_message(
            f"Đã tặng **{gift}** cho {user.mention} 🎉",
            ephemeral=True
        )
        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            # Nếu không thể DM (khóa DM), thì bot sẽ ping thẳng trong channel
            await interaction.followup.send(
                f"{user.mention} đã tặng quà nhưng mình không thể DM. Đây là quà của bạn:",
                embed=embed
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(GiftCog(bot))

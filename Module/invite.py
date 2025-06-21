from utils.ClientUser import ClientUser

from disnake.ext import commands
import disnake

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot: ClientUser = bot


    @commands.command(name="invite", description="Hiển thị liên kết lời mời của tôi để bạn thêm tôi vào máy chủ của bạn.")
    async def invite_legacy(self, ctx: disnake.MessageCommandInteraction):
        if ctx.author.bot:
            return
        await self.invite.callback(self=self, inter=ctx)

    @commands.slash_command(
        description=f"Hiển thị liên kết lời mời của tôi để bạn thêm tôi vào máy chủ của bạn."
    )
    async def invite(self, inter: disnake.AppCmdInter):

        try:
            await inter.response.defer(ephemeral=True)
        except AttributeError:
            pass

        bot = self.bot

        invite = f"[`{disnake.utils.escape_markdown(str(bot.user.name))}`]({disnake.utils.oauth_url(bot.user.id, permissions=disnake.Permissions(37218365729110), scopes=('bot', 'applications.commands'))})"

        embed = disnake.Embed(
            title="Lời mời của tôi",
            description=f"Nhấp vào liên kết bên dưới để thêm tôi vào máy chủ của bạn.\n{invite}",
            color=0xC03865
        )
        embed.set_footer(text="Bot Nhạc", icon_url="https://i.pinimg.com/736x/68/e7/53/68e7537b1c11cf58e171c55463c43b3c.jpg")
        try:
            await inter.edit_original_response(embed=embed)
        except (AttributeError, disnake.InteractionNotEditable):
            await inter.send(embed=embed)

def setup(bot: ClientUser):
    bot.add_cog(Invite(bot))
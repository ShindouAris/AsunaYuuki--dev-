from utils.ClientUser import ClientUser

from disnake.ext import commands
import disnake


class Help(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot: ClientUser = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="help", description="Hiện danh sách lệnh")
    async def help_legacy(self, ctx: disnake.MessageCommandInteraction):
        if ctx.author.bot:
            return
        await self.help.callback(self=self, inter=ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="help", description="Hiện danh sách lệnh")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        if inter.author.bot:
            return
        try:
            await inter.response.defer(ephemeral=True)
        except AttributeError:
            pass

        embed = disnake.Embed()

        embed.title = "ㅤㅤㅤ<a:z2_flower_leaf:1292877806279327836> Menu Lệnh Của Bot Nhạc Discord <a:z41_approvedcheckblack:1292877910063190167>"
        embed.url = "https://discord.gg/uCVYd7KQQR"

        embed.description = f"""<a:z2_lovealarm:1292877840030760982> Menu Lệnh Bot Nhạc Discord <@1368269148660174929> <:monitor:1370019159504588905>
ㅤㅤㅤㅤㅤChủ Bot : <@1299777672905363569> <a:emoji_111:1382214149823791185>
╔═══════════════☆♡☆═══════════════╗
 ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /play | a!play + link nhạc  <a:z2_flower:1292877789531345038>
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /volume từ 5-150 Âm Lượng <a:z2_flower:1292877789531345038>
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /stop Để Tắt Nhạc Của Bot <a:z2_flower:1292877789531345038>
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /loopmode | a!loop Để Lặp Lại Vô Hạn <a:z2_flower:1292877789531345038>
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /next Để Skip Nhạc Bot Đang Phát <a:z2_flower:1292877789531345038>
ㅤ<a:z2_yellowstar:1292877892891574362> Những Lệnh Cơ Bản <a:w1_welcome:1292877700700045406><a:w1_welcome1:1292877719813492767> Khi Dùng Bot Nhạc<a:z2_yellowstar:1292877892891574362>
•❅─────────────────✧❅✦❅✧────────────────❅•
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /about Đẻ Xem Cấu Hình Máy Tính
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /emoji create Để Thêm Emoij 
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /purge Để Xóa Tin Nhắn Nhanh 
ㅤ- <:z4_bluepin:1292877926974488606> Dùng Lệnh /nsfw Tự Tìm Hiểu Nuke 
ㅤㅤ<a:z2_yellowstar:1292877892891574362> Sẽ Có Cập Nhật Thêm Lệnh Và Module Bot <a:z2_yellowstar:1292877892891574362>
•❅─────────────────✧❅✦❅✧────────────────❅•
<a:z2_floatingflowersparkle:1292877771953143809>  Bot Sẽ Có Lúc Tắt Lúc Mở Do Admin Bot Không có <a:z2_floatingflowersparkle:1292877771953143809>
Tiền Thuê Vps Mà dùng Nên Thông Cảm Nhé Xin Cảm Ơn
<a:z41_approvedcheckblack:1292877910063190167> Donate : 9990328421004 CTK : Nguyễn Anh Nhật <a:z41_approvedcheckblack:1292877910063190167>
"""

        embed.colour = 0x07e0d8
        embed.set_footer(text="Menu Bot Nhạc Discord", icon_url="https://i.pinimg.com/736x/ca/ae/5d/caae5db7b709a99939bff027f9eb1206.jpg")


        try:
            await inter.edit_original_response(embed=embed)
        except AttributeError:
            await inter.send(embed=embed)

def setup(bot: ClientUser):
    bot.add_cog(Help(bot))

from disnake import Color, Embed, __version__, AppCmdInter, InteractionNotEditable
from disnake.ext.commands import Cog, slash_command, CooldownMapping, BucketType
from psutil import Process, virtual_memory, cpu_count, cpu_percent
from humanize import naturalsize
from os import getpid
from utils.ClientUser import ClientUser
from platform import system, python_version, release, machine


class Ping(Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot

    @slash_command()
    async def ping(self, ctx):
        embed = Embed(
            title="Pong! Nhà Mạng Viettel",
            description=f"<:BlemiCry:1371175234211811358> API Độ Trễ Của Nhà Mạng Viettel [ditme Viettel]: {round(self.bot.latency * 1000)}ms",
            color= Color.red()
        )
        await ctx.send(embed=embed)
        
    about_cd = CooldownMapping.from_cooldown(1, 5, BucketType.member)
        
    @slash_command(
        description=f"About Me.", cooldown=about_cd, dm_permission=False
    )
    async def about(
            self,
            inter: AppCmdInter
    ):

        await inter.response.defer(ephemeral=True)
        python_ram = Process(getpid()).memory_info().rss

        ram_msg = f"> <:ram:1138360456399028254>  **RAM (Python):** `{naturalsize(python_ram)} \ {naturalsize(virtual_memory()[0])}`\n"
        
        latency_bot = round(self.bot.latency * 1000)

        user = set()

        for users in self.bot.users:
            user.add(users)
            
        embed = Embed(description="", color=0xC03865)

        embed.title = f"<a:z41_approvedcheckblack:1292877910063190167> Máy Chủ Âm Nhạc {self.bot.available_nodes[0].label} - Cấu Hình Máy <:monitor:1370019159504588905>"
        
        embed.description += f"###  Thông tin bot {self.bot.user.name}#{self.bot.user.discriminator}:\n"

        embed.description += f"> <:monitor:1370019159504588905> **Python:** `{python_version()}`\n" \
                             f"> <:monitor:1370019159504588905> **API:** `{__version__}`\n" \
                             f"> <:monitor:1370019159504588905> **OS:** `{system()} {release()} {machine()}`\n" \
                             f"> <:ayakacccng:1310284364218896405> **CPU:** `{cpu_percent()}% \ 100%, ({cpu_count()} Core)`\n" \
                             f"{ram_msg}" \
                             f"> ** <:BlemiCry:1371175234211811358> API Độ Trễ Của Nhà Mạng Viettel [ditme Viettel]:** `{latency_bot}ms`\n" \
                             f"{'=' * 41}\n" \
                             f"> <a:seele_:1336043763012735146> Có Bao Nhiêu Member Thêm Vào Máy Chủ: {len(user)}\n" \
                             f"> <a:ganzurunray:1369322810287325346> **Uptime:** <t:{int(self.bot.uptime.timestamp())}:R>\n" \
                             f"> <a:seele_che:1336043722475049015> Thông Tin Servers: {self.bot.env.get('SERVER_NAME')}\n   "
        
        try:
            await inter.edit_original_message(embed=embed)
        except (AttributeError, InteractionNotEditable):
            try:
                await inter.response.edit_message(embed=embed)
            except:
                await inter.send(embed=embed, ephemeral=True)             


def setup(bot: ClientUser):
    bot.add_cog(Ping(bot))
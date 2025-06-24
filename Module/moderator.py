import disnake
from disnake.ext import commands

from utils.ClientUser import ClientUser


def convert_tm(x: str) -> dict:
    _input = x.lower().strip()
    valid = False
    _time = [0, 0, 0, 0] # [day, hours, minutes, seconds]
    buffer = ""
    for i in _input:
        if i.isnumeric():
            valid = True
            buffer += i
        elif i.isalpha():
            if not buffer.isnumeric(): continue
            if i in ["d"]: _time[0] = int(buffer)
            elif i in ["h"]:  _time[1] = int(buffer)
            elif i in ["m", "p"]: _time[2] = int(buffer)
            elif i in ["s"]: _time[3] = int(buffer)
            buffer = ""
    if buffer.isnumeric(): _time[3] = int(buffer)
    um = _time[0] * 86400 + _time[1] * 3600 + _time[2] * 60 + _time[3]
    return {
        "valid": True, 
        "tm": um
    } if valid else {
        "valid": False,
        "tm": None
    }

class Moderator(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot: ClientUser = bot

    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.slash_command(name="mute", description="Vô hiệu hóa kĩ thuật nói của một thành viên", 
                            options=[
                                disnake.Option(name="member", description="Thành viên cần bị vô hiệu hóa kĩ thuật nói", type=disnake.OptionType.user, required=True),
                                disnake.Option(name="duration", description="Thời gian vô hiệu hóa kĩ thuật nói (giây)", type=disnake.OptionType.integer, required=True),
                                disnake.Option(name="reason", description="Lý do vô hiệu hóa kĩ thuật nói", type=disnake.OptionType.string, required=False)
                                ])
    async def mute(self, interaction: disnake.CommandInteraction, member: disnake.Member, duration: int, reason: str = None):
        try: 
            duration = convert_tm(str(duration))
            if not duration["valid"] or duration["tm"] is None:
                await interaction.response.send_message("Thời gian vô hiệu hóa kĩ thuật nói không hợp lệ. Vui lòng sử dụng định dạng hợp lệ (vd: 1d2h3m4s).", ephemeral=True)
                return
            await member.timeout(duration=duration["tm"], reason=reason)
            await interaction.response.send_message(f"Đã vô hiệu hóa kĩ thuật nói của {member.mention} trong {duration} giây.", ephemeral=True)
        
        
        except disnake.Forbidden:
            await interaction.response.send_message("Tôi không có quyền vô hiệu hóa kĩ thuật nói của thành viên này.", ephemeral=True)
        except disnake.HTTPException:
            await interaction.response.send_message("Đã xảy ra lỗi khi cố gắng vô hiệu hóa kĩ thuật nói của thành viên này.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Đã xảy ra lỗi không xác định: {str(e)}", ephemeral=True)

    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.slash_command(name="kick", description="Sút một thành viên ra khỏi máy chủ",
                            options=[disnake.Option(name="member", description="Thành viên cần bị sút ra", type=disnake.OptionType.user, required=True),
                                     disnake.Option(name="reason", description="Lý do sút thành viên", type=disnake.OptionType.string, required=False)])
    async def kick(self, interaction: disnake.CommandInteraction, member: disnake.Member, reason: str = None):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Đã sút {member.mention} ra khỏi máy chủ.", ephemeral=True)
        except disnake.Forbidden:
            await interaction.response.send_message("Tôi không có quyền sút thành viên này ra khỏi máy chủ.", ephemeral=True)
        except disnake.HTTPException:
            await interaction.response.send_message("Đã xảy ra lỗi khi cố gắng sút thành viên này ra khỏi máy chủ.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Đã xảy ra lỗi không xác định: {str(e)}", ephemeral=True)


def setup(bot: ClientUser):
    bot.add_cog(Moderator(bot))
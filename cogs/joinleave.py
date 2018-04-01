import discord
import datetime


class JoinLeave:
    def __init__(self, bot):
        self.bot = bot
        self.background = "joinleave.png"

    @staticmethod
    def get_joinleave_channel(member):
        """
        Fetches instance of `discord.TextChannel` in
        instance of `discord.Guild` using an instance
        of `discord.Member`.
        """
        return discord.utils.get(member.guild.channels, name='joinleave')

    async def on_member_join(self, member):
        join_embed = discord.Embed(
            title=f"{member} has joined the server.",
            color=discord.Color.green()
        )
        join_embed.add_field(
            name="Join Date:",
            value=f"{member.joined_at} UTC"
        )
        join_embed.add_field(
            name="ID",
            value=f"{member.id}"
        )
        join_embed.add_field(
            name="Account Created At:",
            value=f"{member.created_at} UTC"
        )
        join_embed.set_footer(
            text=f"User Joined | {member.guild.member_count} members",
            icon_url=member.guild.icon_url_as(format='webp', size=1024)
        )
        join_embed.set_thumbnail(url=member.avatar_url)
        await self.get_joinleave_channel(member).send(embed=join_embed)

        await member.add_roles(discord.utils.get(member.guild.roles, name='Elevens [Users]'))

    async def on_member_remove(self, member):
        leave_embed = discord.Embed(
            title=f"{member} has left the server.",
            color=discord.Color.red()
        )
        leave_embed.add_field(
            name="Leave Date:",
            value=f"{datetime.datetime.utcnow()} UTC"
        )
        leave_embed.add_field(
            name="ID",
            value=f"{member.id}"
        )
        leave_embed.add_field(
            name="Account Created At:",
            value=f"{member.created_at} UTC"
        )
        leave_embed.set_footer(
            text=f"User Left | {member.guild.member_count} members",
            icon_url=member.guild.icon_url_as(format='webp', size=1024)
        )
        leave_embed.set_thumbnail(url=member.avatar_url)
        await self.get_joinleave_channel(member).send(embed=leave_embed)


def setup(bot):
    bot.add_cog(JoinLeave(bot))

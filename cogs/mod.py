import asyncio
import json
import discord
from discord.ext.commands import command


class CannotRemoveMember(Exception):
    pass


class Mod:
    """Moderation Commands."""
    def __init__(self, bot):
        self.bot = bot

    def __local_check(self, ctx):
        return discord.utils.get(ctx.guild.roles, name="Mods") in ctx.message.author.roles
    
    def check_user(self, ctx, member: discord.Member):
        mod = discord.utils.get(ctx.guild.roles, name="Mods") in member.roles
        if mod:
            raise CannotRemoveMember("You can't do that, they have the `Mods` role.")
        else:
            return

    @command()
    async def kick(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Kick a user."""
        try:
            self.check_user(ctx, member)
        except CannotRemoveMember as e:
            return await ctx.send(str(e))
        else:
            await member.send(f'You have been kicked for the following issue:\n{reason}')
            await asyncio.sleep(5)
            await member.kick(reason=reason)
            await asyncio.sleep(5)
            await ctx.send(f'Kicked {member} | Reason: {reason}')

    @command()
    async def ban(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Ban a user."""
        try:
            self.check_user(ctx, member)
        except CannotRemoveMember as e:
            return await ctx.send(str(e))
        else:
            await member.send(f'You have been kicked for the following issue:\n{reason}')
            await asyncio.sleep(5)
            await member.ban(reason=reason, delete_message_days=0)
            await ctx.send(f'Banned {member} | Reason: {reason}')

    @command()
    async def softban(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Softban a user."""
        try:
            self.check_user(ctx, member)
        except CannotRemoveMember as e:
            return await ctx.send(str(e))
        else:
            await member.send(f'You have been softbanned for the the following issue:\n{reason}')
            await member.ban(reason=reason, delete_message_days=2)
            await member.unban()
            await ctx.send(f'Softbanned {member} | Reason: {reason}')

    @command()
    async def hackban(self, ctx, member_id: int, *, reason: str="Violation of one or more rules."):
        """Ban a user."""

        if discord.utils.get(ctx.guild.members, id=member_id) is not None:
            await ctx.send(f"Cannot hackban member who is currently in the server.\nPlease use `-ban [member]` instead!")
            return

        member = discord.Object(member_id)
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send(f'Banned user with ID of `{member_id}`')

    @command()
    async def purge(self, ctx, count: int):
        """Purge an amount of messages from a channel."""
        if count <= 1:
            msg = ctx.send('Please input a valid number of messages.')
            await asyncio.sleep(8)
            await msg.delete()
        elif count >= 1:
            deleted_messages = await ctx.channel.purge(limit=(count + 1))
            message_number = max((len(deleted_messages) - 1), 0)
            resp = 'Deleted `{} message{}` 👌 '.format(message_number, ('' if (message_number < 2) else 's'))
            confirm_message = await ctx.send(resp)
            await asyncio.sleep(8)
            await confirm_message.delete()

    @command()
    async def disclaimer(self, ctx):
        message = [
            "The Area 11 Discord:tm: is a space where all users should be happy and comfortable.",
            "Breaking the rules is a violation of that comfort, and though it seems hostile to do so,",
            "the moderator team must enforce the rules."
        ]

        await ctx.send(' '.join(part for part in message))

    @staticmethod
    def get_rule():
        """Fetches `arg` in `./cogs/rules.json`."""
        with open("./cogs/rules.json") as f:
            config = json.load(f)

        return config

    @command(name="rule")
    async def rule_(self, ctx, rule: int):
        """Shows a rule. Only integers are accepted."""
        if rule >= 12:
            await ctx.send(f"There isn't a rule `{rule}`! There are only 11 rules.")
        else:
            await ctx.send(self.get_rule()[f"{rule}"])

    @command(name="presence", aliases=["game", "changegame"])
    async def presence(self, ctx, *, game: str = None):
        if(game == None):
            await self.bot.change_presence(activity=None)
            return
        await self.bot.change_presence(activity=discord.Game(name=game))

def setup(bot):
    bot.add_cog(Mod(bot))

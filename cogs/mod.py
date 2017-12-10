import asyncio
import json
import discord
from discord.ext.commands import command

class Mod:
    """Moderation Commands."""
    def __init__(self, bot):
        self.bot = bot

    def __local_check(self, ctx):
        return discord.utils.get(ctx.guild.roles, name="Mods") in ctx.message.author.roles

    @command()
    async def kick(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Kick a user."""
        await member.send(f'You have been kicked for the following issue:\n{reason}')
        await asyncio.sleep(5)
        await member.kick(reason=reason)
        await asyncio.sleep(5)
        await ctx.send(f'Kicked {member} | Reason: {reason}')

    @command()
    async def ban(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Ban a user."""
        await member.send(f'You have been kicked for the following issue:\n{reason}')
        await asyncio.sleep(5)
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member} | Reason: {reason}')

    @command()
    async def softban(self, ctx, member: discord.Member, *, reason: str="Violation of one or more rules."):
        """Softban a user."""
        await member.send(f'You have been softbanned for the the following issue:\n{reason}')
        await member.ban(reason=reason, delete_message_days=2)
        await member.unban()
        await ctx.send(f'Softbanned {member} | Reason: {reason}')

    @command()
    async def hackban(self, ctx, member_id: int, *, reason: str="Violation of one or more rules."):
        """Ban a user."""
        member_id = discord.Object(member_id)
        await ctx.guild.ban(user=member_id, reason=reason)
        await ctx.send(f'Banned {member_id.name}')

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


def setup(bot):
    bot.add_cog(Mod(bot))

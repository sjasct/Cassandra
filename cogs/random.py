import discord
from discord.ext.commands import command


class Random:
    def __init__(self, bot):
        self.bot = bot

    async def get_image(self, ctx, link: str, name: str):
        image_embed = discord.Embed(
            title=f"{name} Pic!"
        )
        image = ""
        if name is "Cat":
            async with ctx.session.get(link) as r:
                res = await r.json()
                image = res['file']
        if name is "Dog":
            async with ctx.session.get(link) as r:
                res = await r.json()
                image = res['url']
        if name is "Nick's great":
            image = link
        image_embed.set_image(url=image)
        await ctx.send(embed=image_embed)

    @command()
    async def cat(self, ctx):
        """Posts a cat image."""
        await self.get_image(
            ctx, 'http://random.cat/meow', "Cat"
        )

    @command()
    async def dog(self, ctx):
        """Posts a dog image"""
        await self.get_image(
            ctx, 'http://random.dog/woof.json', "Dog"
        )

    @command()
    async def praise_nick(self, ctx):
        """nick's great"""
        await self.get_image(
            ctx, "http://www.mytinyphone.com/uploads/users/acdcslvr/377671.jpg", "Nick's great"
        )

def setup(bot):
    bot.add_cog(Random(bot))

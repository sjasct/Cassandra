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
        image_embed.set_image(url=image)
        await ctx.send(embed=image_embed)

    @command()
    async def cat(self, ctx):
        await self.get_image(
            ctx, 'http://random.cat/meow', "Cat"
        )

    @command()
    async def dog(self, ctx):
        await self.get_image(
            ctx, 'http://random.dog/woof.json', "Dog"
        )


def setup(bot):
    bot.add_cog(Random(bot))
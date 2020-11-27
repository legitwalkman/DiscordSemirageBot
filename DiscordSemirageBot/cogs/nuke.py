import discord
from discord.ext import commands

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def nuke(self, ctx, channel_name):
        channel_id = int(''.join(i for i in channel_name if i.isdigit())) 
        existing_channel = self.bot.get_channel(channel_id)
        if existing_channel:
            await existing_channel.clone(reason="Has been nuked")
            await existing_channel.delete()
            embed = discord.Embed(title='Channel has been nuked')
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'No channel named **{channel_name}** was found')


def setup(bot):
    bot.add_cog(Nuke(bot))
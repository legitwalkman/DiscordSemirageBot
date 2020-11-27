import discord
from discord.ext import commands
import platform

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Commands Cog has been loaded\n-----')


    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        
        embed = discord.Embed(title='Logout Notice')
        embed.add_field(name='Logout',value='FUCK YOU BLACK PEOPLE I AM OUT!')
        
        await ctx.send(embed=embed)
        await self.bot.logout()

    @commands.command()
    async def echo(self, ctx, *, message=None):
    
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def sendembed(self, ctx):

	    embed = discord.Embed(title="Reaction Roles", description="React with :egg: for Egghead Supreme Role.\nReact with :black_medium_small_square: for Black Role.\nReact with :white_medium_small_square: for White Role.\nReact with :man_in_manual_wheelchair: for Disabled Role.",  color=discord.Color.blue())

	    await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))
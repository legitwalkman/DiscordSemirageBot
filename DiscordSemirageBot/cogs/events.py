import discord
from discord.ext import commands, tasks
import random
import datetime


class Events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Events Cog has been loaded\n-----')


    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = discord.utils.get(member.guild.text_channels, name="join-leave")
        if channel:
            embed = discord.Embed(
                description="Another Gipsy joined!",
                color=random.choice(self.bot.color_list),
            )
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)
        role = 'New'
        rank = discord.utils.get(member.guild.roles, name=role) #Bot get guild(server) roles
        await member.add_roles(rank)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = discord.utils.get(member.guild.text_channels, name="join-leave")
        if channel:
            embed = discord.Embed(
                description="See ya retard!",
                color=random.choice(self.bot.color_list),
            )
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
                await ctx.send("You cant use this fool")
        raise error


def setup(bot):
    bot.add_cog(Events(bot))
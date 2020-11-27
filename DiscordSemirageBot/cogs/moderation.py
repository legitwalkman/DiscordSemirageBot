import discord
from discord.ext import commands
import datetime
import asyncio
import re

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 864000}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f'{value} is an invalid time key! h|m|s|d are valid arguments')
            except ValueError:
                raise commands.BadArgument(f'{key} is not a number!')
        return time

class Moderation(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.command(
        name='mute',
        description="Mutes a given user for x time!",
        ussage='<user> [time]'
    )
    #@commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found! Please create one called `Muted`")
            return

        await member.add_roles(role)
        await ctx.send((f"Muted `{member.display_name}` for {time}s." if time else f"Muted `{member.display_name}`."))

        if time:
            await asyncio.sleep(time)

            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted `{member.display_name}`")

    @commands.command(
        name='unmute',
        description="Unmuted a member!",
        usage='<user>'
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found! Please create one called `Muted`")
            return

        if role not in member.roles:
            await ctx.send("This member is not muted.")

        await member.remove_roles(role)
        await ctx.send(f"Unmuted `{member.display_name}`")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await ctx.guild.kick(user=member)

        channel = self.bot.get_channel(781603048052752425)
        embed = discord.Embed(description=f'{ctx.author.name} kicked {member.name}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)

        channel = self.bot.get_channel(781603048052752425)
        embed = discord.Embed(description=f'{ctx.author.name} banned {member.name} for {reason}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def unban(self, ctx, member):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member)

        channel = self.bot.get_channel(781603048052752425)
        embed = discord.Embed(description=f'{ctx.author.name} unbanned {member.name}')
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.command(
        name="purge",
        description="A command which purges the channel it is called in",
        usage="[amount]",
    )
    @commands.guild_only()
    @commands.is_owner()
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title=f"{ctx.author.name} purged: {ctx.channel.name}",
            description=f"{amount} messages were cleared",
        )
        await ctx.send(embed=embed, delete_after=15)


def setup(bot):
    bot.add_cog(Moderation(bot))
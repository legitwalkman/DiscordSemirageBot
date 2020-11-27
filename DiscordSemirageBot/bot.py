import discord
from discord.ext import commands
import logging
from pathlib import Path
import platform
import json
import datetime
import os
from discord.ext import tasks


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f'{cwd}\n-----')

intents = discord.Intents.all()

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix='.', case_insensitive=True, owner_id=336952248984928256, intents=intents)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = 'v1'


bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C, 
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_ready():
    print(f"Logged ins as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: .\n-----")
    data = read_json("blacklist")
    bot.blacklisted_users = data["blacklistedUsers"]
    await bot.change_presence(activity=discord.Game(name=f'Semiraging'))

    bot.reaction_roles = []
 

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    
    if message.author.id in bot.blacklisted_users:
        return

    if message.content.lower().startswith('help'):
        await message.channel.send("Use `.help` you fuck")

    await bot.process_commands(message)

if __name__ == '__main__':
    
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith('.py') and not file.startswith("_"):
            bot.load_extension(f'cogs.{file[:-3]}')

@bot.command()
@commands.is_owner()
async def blacklist(ctx, user: discord.Member):
    if ctx.message.author.id == user.id:
        await ctx.send("Hey, you cannot blacklist yourself!")
        return

    bot.blacklisted_users.append(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

@bot.command()
@commands.is_owner()
async def unblacklist(ctx, user: discord.Member):
    bot.blacklisted_users.remove(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

@bot.event
async def on_raw_reaction_add(payload):
    for role, msg, emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    for role, msg, emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@bot.command()
async def set_reaction(ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role, msg, emoji))

    else:
        await ctx.send('invalid arguments')

def read_json(filename):
    with open(f'{cwd}/bot_config/{filename}.json','r') as file:
        data = json.load(file)

    return data

def write_json(data, filename):
    with open(f'{cwd}/bot_config/{filename}.json','w') as file:
        json.dump(data, file, indent=4)

bot.run(bot.config_token)
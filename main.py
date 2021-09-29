import os
import discord
import typing
import random
import json
import re 
import requests
import discord.utils
from discord.ext import commands
DISCORD_TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.members=True
#Prefix
bot = commands.Bot('!', intents=intents, case_insensitive=True)

#Status
@bot.event
async def on_ready():
    print(f'{bot.user} har aktiverats & är aktiv i discord!')

    await bot.change_presence(activity=discord.Game(name="Dizer.se"))

#Tar bort vanliga hjälp menyn
bot.remove_command("help")

#Lägger till nytt hjälp kommand & meny
@bot.group(invoke_without_command=True, aliases=['hjälp'])
async def help(ctx):
 em = discord.Embed(title = "🔧 Hjälp 🔧", description = "> Här hittar du en lista med de kommands som finns tillgängliga!")

 em.add_field(name = "Generella kommands:", value = "!förslag (!förslag <text>) | !lystring (!lystring <text>) | !inspiration (Inspirerande citat) | !rensa (!rensa <antal> **OBS: Skriver du bara !rensa försvinner __ALLT__ i kanalen!**")

 await ctx.send(embed = em)

#Välkommst meddelande
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(892508023250112613) #Kanal ID
    embed=discord.Embed(title=f"**Välkommen {member.name}!** 🥳", description=f"Roligt att du är här! Hoppas du trivs! 💎")
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)

#Auto Roll
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Dizer') #Bestäm Roll
    await member.add_roles(role)

#Förslag
@bot.command()
async def förslag(ctx, *, message): 
    await ctx.message.delete()
    msg = await ctx.send(message)
    msg = await ctx.send("`Föreslaget" + " av:`" + ctx.author.mention)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

#Inspiration (API)
@bot.command()
async def inspiration(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)
    
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#Lystring / @everyone
@bot.command()
async def lystring(ctx, *, message): 
    await ctx.message.delete()
    msg = await ctx.send("`Lystring!`")
    msg = await ctx.send(message)
    msg = await ctx.send('@everyone')

#Rensa
@bot.command(aliases= ['rensa','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount :int = -1):
   if amount == -1:
       await ctx.channel.purge(limit=1000000)
   else:
       await ctx.channel.purge(limit=amount)
      

bot.run(os.environ['TOKEN'])
import random
import discord.ext
from discord.ext import commands

client = discord.Client()

client = commands.Bot(command_prefix='!')  # put your own prefix here

f=open("list.txt",encoding="utf8")
content = f.readlines()
@client.event
async def on_ready():
    print("bot online") 

@client.command()
async def roastme(ctx):
    await ctx.send(str(content[random.randint(0, 170)]))  

client.run("TOKEN")

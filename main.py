
#   import libs
import random
import discord.ext
from discord.ext import commands
import discord
import youtube_dl
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import asyncio
import sqlite3
import requests
from bs4 import BeautifulSoup as bf
import time

#   create discord client
client = discord.Client()
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

#   set prefix statue and activity
activity= discord.Activity(type=discord.ActivityType.watching, name="DEAD BEEF")
client = commands.Bot(command_prefix='33k!' , activity=activity, status=discord.Status.idle ,help_command = help_command) 

#   ready event
@client.event
async def on_ready():
    print("bot online")

#   screenshots command
@client.command(name= "screenshot" ,aliases=["sc"], help="Get you a random funny screanshot of 33k team members")
async def screen(ctx):
    #   get a random screenshot
    num=random.randrange(0, 39)
    try:
        await ctx.send("hhhh ad7kou 3lih", file=discord.File("aka/Capture{}.png".format(num)))
    except:
        #   catch exception if image is not png
        await ctx.send("hhhh ad7kou 3lih", file=discord.File("aka/Capture{}.jpg".format(num)))

#   roast command
@client.command(name="roast",aliases=["roastme","r"] , help="Get you funny roasting quotes")
async def roast(ctx):
    #   open list of roasting sentence
    f=open("list.txt",encoding="utf8")
    content = f.readlines()
    num = random.randint(0, 170)
    await ctx.send(str(content[num]))  

#   join function for music
@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    #   if user is note in voice channel 
    if not ctx.message.author.voice:
        await ctx.send("<@{}> is not connected to a voice channel".format(ctx.message.author.id))
        await ctx.send("try to join a voice channal and try again")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

#   leave function for music
@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("***The bot is not connected to a voice channel.***")
    except:
        await ctx.send("***The bot is not connected to a voice channel.***")

#   play music
@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['p, pl'])
async def play(ctx, url=None):
    # ctx.command = client.get_command("join")
    # await client.invoke(ctx) 
    if url==None:
        await ctx.send("You need to pass a youtube link with the command")
        await ctx.send("Ex: 33k!play https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    else:
        url=str(url)
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music end or use the 'stop' command")
            return
        await ctx.send("Getting everything ready, playing audio soon")
        print("Someone wants to play music let me get that ready for them...")
        voice = get(client.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

# a=output[0][1]
# print(a)

#   flag command
@client.command(name="flag", help="Simple flag guessing game")
async def flag(ctx): # add reaction answers using country name
    #   connect to database of flags 
    conn = sqlite3.connect('flags.db')
    cursor_obj = conn.cursor()

    #   select random flag
    statement ='SELECT * FROM FLAGS ORDER BY RANDOM() LIMIT 1;'
    cursor_obj.execute(statement)
    output = cursor_obj.fetchall()
    await ctx.send(output[0][1])
    await ctx.send("**Guess the flag**")
    print(output[0][0])
    try:
        msg = await client.wait_for("message", timeout=30) 
        if str(msg.content).lower()==str(output[0][0]).lower().replace(".", ""):
            msg1=await ctx.send("**Correct!**")
            await msg1.add_reaction( emoji= "✅")
        else:
            msg1=await ctx.send("**wrong answer!!**")
            await msg1.add_reaction( emoji= "❌")
            await ctx.send("*** correct answer is {} ***".format(output[0][0])) #    add reaction for re question 
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")

#   quiz command
@client.command(name= "quiz" , aliases=['q', 'question'], help="Simple question game")
async def quiz(ctx):  # add second parameter for category // category : str
    # if category==None :
    #     await ctx.send("you need to pass a parameter Ex: general, sports ...")
    #     return 
    alpha={"A":"1️⃣","B":"2️⃣","C":"3️⃣","D":"4️⃣"}
    categories_links= {"general":"http://www.indiabix.com/general-knowledge/basic-general-knowledge/005001",
                        "sports":"http://www.indiabix.com/general-knowledge/sports/",
                        "science":"http://www.indiabix.com/general-knowledge/general-science/",
                        "geography":"http://www.indiabix.com/general-knowledge/world-geography/",
                        "technology":"http://www.indiabix.com/general-knowledge/technology/",
                        "inventions":"http://www.indiabix.com/general-knowledge/inventions/"
                        
    }
    def check(reaction, user):
        return user == ctx.author
    num1=random.randrange(2, 12)
    num2=random.randrange(0, 5)
    url=  "http://www.indiabix.com/general-knowledge/basic-general-knowledge/00500"+str(num1) # categories_links[category]
    r= requests.get(url)
    content = r.content
    soup = bf(content,'html.parser')
    questions=soup.find_all('td', {'class': 'bix-td-qtxt'})
    choices= soup.findAll("td", {"width" : "99%"})
    answers= soup.find_all('span', {'class': 'jq-hdnakqb mx-bold'})
    j=0
    for i in questions:
        if questions.index(i) != num2:
            j=j+4
            continue
        else:
            quiz=await ctx.send(" > **You have 30 seconds to answer**\n"
                " > **Question:** "+str(i.text)
            +"\n > "+"1️⃣-"+str(choices[j].text)+"\n > "+"2️⃣-"+str(choices[j+1].text)+"\n > "+"3️⃣-"+str(choices[j+2].text)+'\n > '+"4️⃣-"+str(choices[j+3].text)+'\n'
            )
            
            await quiz.add_reaction(emoji="1️⃣")
            await quiz.add_reaction(emoji="2️⃣")
            await quiz.add_reaction(emoji="3️⃣")
            await quiz.add_reaction(emoji="4️⃣")
            time.sleep(2)
            print("**Question:** "+str(i.text))
            print ("\n"+"1️⃣-"+str(choices[j].text)+"\n"+"2️⃣-"+str(choices[j+1].text)+"\n"+"3️⃣-"+str(choices[j+2].text)+'\n'+"4️⃣-"+str(choices[j+3].text)+'\n')
            print("correct answer is : "+ alpha[str(answers[questions.index(i)].text)]+ "\n")
            j=j+4
            #   reaction answers
            try:
                reaction = await client.wait_for("reaction_add" , timeout=30 , check=check)  # Wait for a reaction
                # print(reaction[0])
                # print(alpha[str(answers[questions.index(i)].text)])
                if ( str(reaction[0]) == str(alpha[str(answers[questions.index(i)].text)]) ):
                    msg1=await ctx.send("**correct answer!!**")
                    await msg1.add_reaction( emoji= "✅") 
                else:
                    msg1=await ctx.send("**wrong answer!!**")
                    await msg1.add_reaction( emoji= "❌")
            except asyncio.TimeoutError:
                msg1=await ctx.send("**Sorry, you didn't reply in time!!**")
                await msg1.add_reaction(emoji="🕛")

            #   this part is for writing answers 
            # try:
            #     msg = await client.wait_for("message", timeout=30) # 30 seconds to reply
            #     if str(msg.content).lower()==str(answers[questions.index(i)].text).lower():
            #         msg1=await ctx.send("correct!")
            #         await msg1.add_reaction( emoji= alpha["A"]) #✅
            #     else:
            #         msg2= await ctx.send("wrong answer !! \n correct answer is : "+ str(answers[questions.index(i)].text)+" \N{SLIGHTLY SMILING FACE}")
            #         await msg2.add_reaction( emoji= "❌")
            # except asyncio.TimeoutError:
            #     await ctx.send("Sorry, you didn't reply in time!")
            #     await ctx.send("try again")

@client.command(name= "TruthOrDare" , aliases=['tord'], help="truth or dare game usage `33k!tord`")
async def TruthOrDare(ctx,tord=None):
    if tord==None:
        await ctx.send("You need to pass a parameter ex: `33k!tord t`")
    elif tord.lower()=="t" or tord.lower()=="truth":
        f=open("Truth.txt","r")
        content=f.readlines()
        num1=random.randrange(0, len(content)+1)
        await ctx.send("***"+content[num1]+"***")
    elif tord.lower()=="d" or tord.lower()=="dare":
        f=open("dare.txt","r")
        content=f.readlines()
        num1=random.randrange(0, len(content)+1)
        await ctx.send("***"+content[num1]+"***")
    else:
        await ctx.send("Parameter is not valid try `33k!tord t` or `33k!tord d`")
        # url = "https://parade.com/966507/parade/truth-or-dare-questions/"
    # request = requests.get(url)
    # content = request.content
    # soup = bf(content, "html.parser")
    # div = soup.find('div', {'class': 'm-detail--body'})
    # children = div.findChildren("p" , recursive=False)
    # await ctx.send(children[num1].text)
    # counter=0
    # numbers=[0,1,2]
    # for i in children:
    #     if counter in numbers or counter==261:
    #         pass
    #     elif counter <= 260:
    #         print('truth: '+ i.text + "\n")
    #     else:
    #         print("dare: "+ i.text + "\n")
    #     counter=counter+1

    
@client.command(name='userinfo',help='get user info ')
async def userinfo(ctx, member: discord.Member):
    embed=discord.Embed(title="<@{}>".format(member.id), url="", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)
    created_at = member.created_at.strftime("the user <@{}> join discord in :".format(member.id)+"%b %d, %Y") #  user join date
    await ctx.send(created_at)
    await ctx.send("the user <@{}> has the following roles:".format(member.id))
    roles=""
    counter=0
    for i in member.roles:
        if counter != 0 :
        #role = get(member.roles, id=i.id)
            roles=roles+ "<@&"+str(i.id)+"> , "
        counter = counter + 1
    await ctx.send(roles)
    #await ctx.send(ctx.guild.roles) # get user all roles
    #discord.member.Permissions()
    counter2=0
    async for i in ctx.channel.history(limit=None):
        if member.id== i.author.id:
            counter2=counter2+1
    await ctx.send("The user <@{}> send {} message".format(member.id,counter2))

@client.command(name= 'ping', help="Get the BOT latency")
async def ping(ctx):
    await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')












client.run("OTY3Njg4OTgwMTYwMjEzMDcz.GZ4KEx.tR49K21mqcaUGGRFJDAoKqjE5eTV5e0ZD76ye8")
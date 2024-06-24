from urllib import request
import discord
import asyncio
from discord.ext import commands
import discord
import random
import os
import json
import time
import datetime
from replit import db, Database
from PIL import Image
import deeppyer

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", case_insensitive=True, intents=intents)



@bot.event
async def on_member_join(member):
    #check how they joined the server
    if member.guild.id ==834159143627522110:
        role = discord.utils.get(member.guild.roles, name="newbies")
        await member.add_roles(role)
@bot.event
async def on_ready():
    print(f"Listening as {bot.user.name}")
    channel = bot.get_channel(855479247426551818)
    await channel.edit(name=f'Member count: {channel.guild.member_count}')
    await bot.change_presence(activity=discord.Game(name="-help"))
@bot.command(name="set",description="Set a variable",brief="Set a variable")
async def set(ctx):
    #create a json variable to store "exp" and "level" and cash as floats
    user_data = '{"exp": 0, "level": 1, "cash": 0}'
    #create a json variable to store the user's id
    user_id = ctx.author.name
    db[user_id] = user_data
    await ctx.send("Variable set!")

@bot.command(name="beg",description="Beg for money",brief="Beg for money")
async def beg(ctx):
    number = random.randint(0,10)
    money = db[ctx.author.name]
    #parse variable money with json.loads
    money = json.loads(money)
    xp = money["exp"]
    lv = money["level"]
    moneys = money["cash"]

    if number == 0:
        moneys = moneys - 5
        await ctx.send("You lost 5 dollars!")
    else:
        moneys = moneys + number
        await ctx.send("You got {} dollars!".format(number))
    xp = xp + 1
    send = db[ctx.author.name]
    send = json.loads(send)
    send["exp"] = xp
    send["cash"] = moneys
    send["level"] = lv 
    #get the level of the user

    
    db[ctx.author.name] = json.dumps(send)

@bot.command(name="check",description="Check your stats",brief="Check your stats")
async def check(ctx):
    money = db[ctx.author.name]
    money = json.loads(money)
    xp = money["exp"]
    cash = money["cash"]
    level = money["level"]
    await ctx.send("You have {} xp level {} and {} dollars!".format(xp,level,cash))

@commands.cooldown(1, 300, commands.BucketType.user)
@bot.command(name="steal",description="Steal money from someone",brief="Steal money from someone")
async def steal(ctx, member: discord.Member):
    money = db[ctx.author.name]
    money = json.loads(money)
    xp = money["exp"]
    cash = money["cash"]
    money2 = db[member.name]
    money2 = json.loads(money)
    xp2 = money2["exp"]
    cash2 = money2["cash"]
    if xp >= 10:
        if cash2 >= 5:
            cash = cash + 5
            cash2 = cash2 - 5
            xp = xp - 10
            xp2 = xp2 + 1
            db[ctx.author.name] = json.dumps({"exp":xp,"level": money["level"],"cash":cash})
            db[member.name] = json.dumps({"exp":xp2,"level": money2["level"],"cash":cash2})
            await ctx.send("You stole 5 dollars from {}!".format(member.name))
        else:
            await ctx.send("{} does not have enough money!".format(member.name))
    else:
        await ctx.send("You do not have enough xp!")
@beg.error
async def steal_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = f'This command is ratelimited, please try again in {round(error.retry_after,1)}s'
        await ctx.send(msg)
    else:
        raise error

@bot.command(name="work",description="turn exp into cash",brief="turn exp into cash")
async def work(ctx):
    money = db[ctx.author.name]
    money = json.loads(money)
    xp = money["exp"]
    cash = money["cash"]
    cash = cash + xp
    xp = xp - xp
    db[ctx.author.name] = json.dumps({"exp":xp,"cash":cash})
    await ctx.send("You earned {} dollars!".format(cash))
@bot.command(name="levelup",description="level up",brief="level up")
async def levelup(ctx):
    money = db[ctx.author.name]
    money = json.loads(money)
    xp = money["exp"]
    level = money["level"]
    if xp >= 100:
        xp = xp - 100
        level = level + 1
        db[ctx.author.name] = json.dumps({"exp":xp,"level":level})
        await ctx.send("You leveled up to level {}!".format(level))
    else:
        await ctx.send("You do not have enough xp!")
@bot.command(name="leaderboard",description="leaderboard",brief="leaderboard")
async def leaderboard(ctx):
    #create a list to store the users
    user_list = []
    #create a list to store the levels
    level_list = []
    #create a list to store the xp
    xp_list = []
    #create a list to store the cash
    cash_list = []
    #get all the users
    users = db.keys()
    #for each user
    for user in users:
        #get the user's data
        data = db[user]
        #parse the data with json.loads
        data = json.loads(data)
        #add the user's data to the list
        user_list.append(user)
        level_list.append(data["level"])
        xp_list.append(data["exp"])
        cash_list.append(data["cash"])
    #create a list to store the sorted users
    sorted_users = []
    #create a list to store the sorted levels
    sorted_levels = []
    #create a list to store the sorted xp
    sorted_xp = []
    #create a list to store the sorted cash
    sorted_cash = []
    #for each user
    for user in user_list:
        #find their index
        index = user_list.index(user)
        #add their index to the sorted lists
        sorted_users.append(index)
        sorted_levels.append(level_list[index])
        sorted_xp.append(xp_list[index])
        sorted_cash.append(cash_list[index])
    #sort the lists
    sorted_users.sort()
    sorted_levels.sort()
    sorted_xp.sort()
    sorted_cash.sort()
    #create a list to store the sorted users
    
    #create a list to store the sorted levels
    sorted_levels = []
    #create a list to store the sorted xp
    sorted_xp = []
    embed = discord.Embed(title="leaderboard", description="Help command", color=0x00ff00)
    

    for user in sorted_users:
        embed.add_field(name=user_list[user], value=cash_list[user], inline=False)
    await ctx.send(embed=embed)
@bot.command(name="gamble",description="gamble",brief="gamble")
async def gamble(ctx, number: int):
    money = db[ctx.author.name]
    money = json.loads(money)
    xp = money["exp"]
    cash = money["cash"]
    if cash >= number:
        if random.randint(0,1) == 0:
            cash = cash + number
            await ctx.send("You won {} dollars!".format(number))
        else:
            cash = cash - number
            await ctx.send("You lost {} dollars!".format(number))
    else:
        await ctx.send("You do not have enough money!")
    db[ctx.author.name] = json.dumps({"exp":xp,"cash":cash,"level":money["level"]})
@bot.command(name="kick",description="kick someone",brief="kick someone")
async def kick(ctx, member: discord.Member):
    if ctx.author.guild_permissions.kick_members:
        await member.kick()
        await ctx.send("{} has been kicked!".format(member.name))
    else:
        await ctx.send("You do not have the correct permissions!")
@bot.command(name="ban",description="ban someone",brief="ban someone")
async def ban(ctx, member: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        await member.ban()
        await ctx.send("{} has been banned!".format(member.name))
    else:
        await ctx.send("You do not have the correct permissions!")
@bot.command(name="unban",description="unban someone",brief="unban someone")
async def unban(ctx, member: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        await ctx.guild.unban(member)
        await ctx.send("{} has been unbanned!".format(member.name))
    else:
        await ctx.send("You do not have the correct permissions!")
@bot.command(name="mute",description="mute someone",brief="mute someone")
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name="muted")
        await member.add_roles(role)
        await ctx.send("{} has been muted!".format(member.name))
    else:
        await ctx.send("You do not have the correct permissions!")

@bot.command(name="coolify")
async def coolify(ctx,user:discord.Member=None):
	if user == None:
		user = ctx.author
	user.avatar_url.save("profile.png")
	img = await Image.open("profile.png")
	try:
		img = await deeppyer.deepfry(img,flares=True)
	except:
		img = await deeppyer.deepfry(img,flares=False)
	await ctx.send(file=discord.File("profile.png"))

@bot.command(name="deepfry")
async def deepfry(ctx):
	try:
		img = ctx.message.attachments[0]
	except:
		await ctx.send("it looks like you don't have a attachment")
	await img.save("meme.png")
	img = Image.open("meme.png")
	try:
		image = await deeppyer.deepfry(img,flares=True)
	except:
		image = await deeppyer.deepfry(img,flares=False)
	image.save("memed.png")
	await ctx.send(file=discord.File("memed.png"))



bot.run(os.environ["key"])

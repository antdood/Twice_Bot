import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
from db import db
from members import hasAllMembers, getAllNicks, nickToName, isMember
from pathlib import Path
from collections import defaultdict
import rankings

def getFile(path, mode = "r"):
    cdir = Path(__file__).resolve().parent

    return open(cdir / path, mode)

def isDiscTag(string):
    return re.search("^<@!?\d+>$", string)

def isMemberShift(string):
    regex = f'(?i)^({"|".join(getAllNicks())})[+-]\d*$'
    return re.search(regex, string)

def discTagToID(tag):
    # Could user discord's converter here but why? Non critical stuff + would need to await for stuff
    charsToBeRemoved = ["<", "@", "!", ">"]

    for c in charsToBeRemoved:
        tag = tag.replace(c, "")

    return tag

async def showRanking(user, channel):
    rankings = db.getRankings(user.id)
    
    displayName = user.nick or user.name

    if rankings:
        text = f"__Rankings of **{displayName}**__\n\n"

        for i, member in enumerate(rankings):
            text += f"{i+1}. {member[0]}\n"

        await channel.send(text)
    else:
        await channel.send(f"**{displayName}** has yet to set their rankings")
    return

async def showGlobalRankings(channel, mode = "default"):
    for msg in rankings.generateGlobalRankingText(mode):
        await channel.send(msg)

async def NANI(channel):
    await channel.send("The fuck you trying to do mate")

load_dotenv()

TOKEN = os.getenv("discord_token")
bot = commands.Bot(command_prefix="!", help_command=None)

@bot.event
async def on_ready():
    print("Logged in.")
    db()

@bot.command(aliases = ['rankings'])
async def ranking(msg, *args):

    if(not args):
        await showRanking(msg.author, msg.channel)          

    elif(len(args) == 1 and isDiscTag(args[0])):
        #For loop here is superfluous. Using msg.message.mentions[0] is identical
        for user in msg.message.mentions:
            await showRanking(user, msg.channel)

    elif(len(args) == 1 and args[0] == "perfect"):
        rankedList = rankings.getMemberScores().keys()

        a = ["Nayeon", "Sana", "Dahyun", "Mina", "Tzuyu", "Momo", "Jihyo", "Chaeyoung", "Jeongyeon"]

        userIDsRaw = db.getUserIDsWithRanking(a)

        userIDs = []

        # This is just for ease of working with MySQLdb return types
        for userThing in userIDsRaw:    
            userIDs.append(userThing[0])

        print(userIDs)

        for userID in userIDs:
            user = await bot.fetch_user(userID)
            print(user.id)
            print(user.name)
            print(user.created_at)
            await user.send("hi")

        # get users that has rankings from db

    elif(len(args) == 9 and hasAllMembers(args)):
        db.newRankings(msg.author.id, args)
        await showRanking(msg.author, msg.channel)
      
    elif(all(map(lambda x : isMemberShift(x), args))):
        if(db.userHasRankings(msg.author.id)):
            for a in args:
                # No need for validation here as that's done in isMemberShift
                nick = re.findall("^\w+", a)[0]
                operation = re.findall("[+-]", a)[0]
                amount = int(re.findall("(?<=[+-])\d*", a)[0] or 1)

                db.shiftRanking(msg.author.id, nick, operation, amount)
            await showRanking(msg.author, msg.channel)
        else:
            await msg.channel.send("Please set your initial rankings before trying to change them. !help for more info.")

    else:
        await NANI(msg.channel)

@bot.command(aliases = ['stat'])
async def stats(msg, *args):

    if(not args):
        await showGlobalRankings(msg.channel, "default") 

    elif(len(args) == 1):
        if(args[0] in ["avg", "average"]):
            await showGlobalRankings(msg.channel, "average")
        elif(args[0] in ["full", "all"]):
            await showGlobalRankings(msg.channel, "full")
        elif(member := isMember(args[0])):
            await showGlobalRankings(msg.channel, args[0])
        else:
            print("this")
            await NANI(msg.channel)

    else:
        await NANI(msg.channel)

@bot.command()
async def help(context):
    with getFile("templates/help.md") as f:
        await context.channel.send(f.read())

@bot.command(aliases = ['credit'])
async def credits(context):
    with getFile("templates/credits.md") as f:
        await context.channel.send(f.read().format("<@158010930200838144>"))

bot.run(TOKEN)

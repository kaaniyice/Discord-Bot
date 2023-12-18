import discord
from discord.ext import commands
from discord import Interaction
import os
import sys
import asyncio
import random
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
LOL_HEROES = os.getenv("LOL_HEROES", None)
SPYFALL_PLACES = os.getenv("SPYFALL_PLACES", None)
GUILD_ID = os.getenv("GUILD_ID", None)

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
random.seed()


# General send message
async def send_user_message(user, string):
    """
    general send message command.
    :param user: discord.utils.get(bot.guilds[0].members, name=str(name))
    :param string: the string to send
    :return: None
    """
    try:
        await user.send(string)
    except discord.Forbidden:
        print(f"Error sending DM to user {user.name}: User has DMs disabled.")
    except discord.HTTPException:
        print(f"Error sending DM to user {user.name}: Bot has no permission to send DMs.")
    except:
        print(f"There was an error sending message to {user.name}")


@bot.event
async def on_ready():
    print(f"{bot.user.name} is loggen in.")


# Command for hello
@bot.command(name='hello', help='says hello to current server/channel')
async def hello(ctx):
    await ctx.send(f"Hello {bot.guilds[0]} server")


@bot.command(name='greet', help='greets the user')
async def greet(ctx):
    await ctx.send(f"Hi, {ctx.message.author.global_name}")


# Command for DND
@bot.command(name='dice', help='rolls a dice in between 1 - given value')
async def dice(ctx, num=6):
    try:
        num = int(num)
    except ValueError:
        await ctx.send(f"Usage: .dice number")
    else:
        number = random.randint(1, num)
        await ctx.send(f"Dice: {number}")


# Command for checking direct message control of author
@bot.command(name='directmessage', help='says Hello via DM message to user')
async def directmessage(ctx):
    try:
        await ctx.message.author.send("Hello")
    except discord.Forbidden:
        print(f"Error sending DM to user : User has DMs disabled.")
    except discord.HTTPException:
        print(f"Error sending DM to user : Bot has no permission to send DMs.")


# Command for choosing a list of things
@bot.command(name='choose', help='chooses one variable in a given list')
async def choose(ctx, *options):
    opt = [i for i in options]
    await ctx.send(random.choice(opt))


@bot.group(name='spyfall', help='spyfall game to play usage: .spyfall start @1person @2person @3person')
async def spyfall(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"Usage: .spyfall start  OR  .spyfall places")


@spyfall.command(name='start', help='spyfall game to play usage: .spyfall start @person @2.person @3.person')
async def start(ctx, *who: discord.Member):
    members = [i for i in who]
    if not len(members) > 0:
        await ctx.send("Usage: .spyfall start @person @2.person @3.person")
        return
    chosen_index = random.randint(0, len(members) - 1)
    spy = members[chosen_index]
    remaining_members = members[:chosen_index] + members[chosen_index + 1:]
    with open(SPYFALL_PLACES, 'r') as f:
        spyfall_places = f.readlines()
        place = random.choice(spyfall_places)
    not_spy = f"You are ||**not the Spy**|| and the place is ||**{place}**||"
    spy_message = f"You are ||**theeee Spy**|| and the place is ||**Unknown**||"
    for member in remaining_members:
        user = discord.utils.get(bot.guilds[0].members, name=str(member))
        if user:
            await send_user_message(user, not_spy)
    user = discord.utils.get(bot.guilds[0].members, name=str(spy))
    await send_user_message(user, spy_message)
    spyfall_places_string = "".join(str(element) for element in spyfall_places)
    await ctx.send(f"```{spyfall_places_string}```")


@spyfall.command(name='places', help='shows places, usage: .spyfall places')
async def places(ctx):
    with open(SPYFALL_PLACES, 'r') as f:
        spyfall_places = f.readlines()
    spyfall_places_string = "".join(str(element) for element in spyfall_places)
    await ctx.send(f"```{spyfall_places_string}```")


# Command for Spyfall lol like game in bot
@bot.command(name='spylol', help='spylol game to play usage: .spylol @person @2.person @3.person')
async def spylol(ctx, *who: discord.Member):
    members = [i for i in who]
    chosen_index = 0
    with open(LOL_HEROES, 'r') as f:
        heroes = f.readlines()
        for _ in range(len(members)):
            selected = discord.utils.get(bot.guilds[0].members, name=str(members[chosen_index]))
            hero = random.choice(heroes)
            for member in members:
                if not member == members[chosen_index]:
                    user = discord.utils.get(bot.guilds[0].members, name=str(member))
                    if user:
                        stringg = f"**{user.global_name}**, **{selected.global_name}**'s hero is : **{hero}**"
                        await send_user_message(user, stringg)
            chosen_index += 1


@bot.command(name='clear', help='this command will clear msgs')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=(amount + 1))
    await ctx.send(f"Cleared **{amount}** messages")


bot.run(BOT_TOKEN)

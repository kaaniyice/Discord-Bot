import discord
from discord.ext import commands
from discord import Interaction
from dotenv import load_dotenv
import os
import random

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user.name} is loggen in.")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {bot.guilds[0]} server")


@bot.command()
async def greet(ctx):
    await ctx.send(f"Hi, {ctx.message.author.global_name}")


# Command for checking direct message control of author
@bot.command()
async def directmessage(ctx):
    try:
        await ctx.message.author.send("Hello")
    except discord.Forbidden:
        print(f"Error sending DM to user : User has DMs disabled.")
    except discord.HTTPException:
        print(f"Error sending DM to user : Bot has no permission to send DMs.")


# Command for choosing a list of things
@bot.command()
async def choose(ctx, *options):
    opt = [i for i in options]
    await ctx.send(random.choice(opt))


# Command for rand select dice
@bot.command()
async def dice(ctx, num=6):
    try:
        num = int(num)
    except ValueError:
        await ctx.send(f"Usage: .dice number")
    else:
        number = random.randint(1, num)
        await ctx.send(f"Dice: {number}")


bot.run(BOT_TOKEN)

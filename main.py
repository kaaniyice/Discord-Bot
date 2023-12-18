import discord
from discord.ext import commands
from discord import Interaction
from dotenv import load_dotenv
import os

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


bot.run(BOT_TOKEN)
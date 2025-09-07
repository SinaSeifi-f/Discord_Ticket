import discord
from discord.ext import commands
import asyncio
import utils.config as config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

async def main():

    await bot.load_extension("cogs.ticket")
    await bot.load_extension("cogs.panel")
    
    await bot.start(config.TOKEN)

asyncio.run(main())

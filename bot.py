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
    print("Loaded commands:", [c.name for c in bot.commands])

async def main():
    bot.load_extension("cogs.ticket")
    bot.load_extension("cogs.panel")

    async with bot:
        await bot.start(config.TOKEN)

asyncio.run(main())

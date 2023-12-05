from json import load
import discord
from discord.ext import commands
from basemodels import Quote
from database import database, quotesDB
import datetime
import random

def get_discord_token_json():
    with open("config.json") as json_file:
        data = load(json_file)
        return data.get("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command(name='quote', help='Get a random quote from the database')
async def quote(ctx):
    # Get Random quote from Database
    query = quotesDB.select()
    result = await database.fetch_all(query)
    quote = random.choice(result)
    await ctx.send(quote.quote)


DISCORD_TOKEN = get_discord_token_json()
bot.run(DISCORD_TOKEN)

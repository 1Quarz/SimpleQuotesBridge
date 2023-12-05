from json import load
import discord
from basemodels import Quote
from database import database, quotesDB
import datetime
import random

def get_discord_token_json():
    with open("config.json") as json_file:
        data = load(json_file)
        return data.get("DISCORD_BOT_TOKEN")

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
        #Load Channel Name and Guild ID from json config file
        with open("config.json") as json_file:
            json_data = load(json_file)
            self.guild_id = json_data.get("GUILD_ID")
            self.channel_name = str(json_data.get("CHANNEL_NAME")).lower()

        # Find the server/Guild based on the ID
        guild = discord.utils.get(self.guilds, id=self.guild_id)

        if guild:
            # Check if the channel already exists
            existing_channel = discord.utils.get(guild.text_channels, name=self.channel_name)
            if not existing_channel:
                # Create the channel if it doesn't exist
                await guild.create_text_channel(self.channel_name)
                print('Channel {} created.'.format(self.channel_name))
        else:
            print('Guild {} not found.'.format(self.guild_id))


    async def on_message(self, message):

        if message.channel.type == discord.ChannelType.private:
            return

        # Check if the message is from the "quotes" channel
        if message.channel.name == self.channel_name:
            # Logic for handling messages in the "quotes" channel goes here
            # For example, you can check for specific content and respond accordingly
            if message.content.startswith('!quote'):
                #Get Random quote from Database
                query = quotesDB.select()
                result = await database.fetch_all(query)
                quote = random.choice(result)
                await message.channel.send(quote.quote)
                

            if message.content.startswith("!add"):
                #Split string after !add 
                split = message.content.split(" ")
                new_quote = Quote(quote=split[1], author=message.author.name)
                
                try:
                    #Insert into database
                    query = quotesDB.insert().values(quote=new_quote.quote, author=new_quote.author, timestamp=datetime.datetime.now())
                    last_record_id = await database.execute(query)
                    await message.channel.send("Quote added")
                except Exception as e:
                    #If UNIQUE constraint is violated
                    await message.channel.send("Quote already exists")
                    
                    

DISCORD_TOKEN = get_discord_token_json()
intents = discord.Intents.default()
intents.dm_messages = True
intents.messages = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)

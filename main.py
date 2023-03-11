import discord
import pytz
import asyncio
from datetime import datetime
from discord.ext import commands, tasks

intents = discord.Intents(
    message_content= True,
    messages= True,
    guilds= True
)

bot = commands.Bot(command_prefix='-', intents=intents)
channel_id = 1079893176552280074

@tasks.loop(seconds=1)
async def timeCheck():
    now_utc = datetime.now(pytz.utc)

    if datetime.today().weekday() == 0:
        if now_utc.hour == 12 and now_utc.minute == 0:
            try:
                channel = bot.get_channel(channel_id)
                await channel.send('Hello everyone! It is Group-hug Monday today! I hope you\'re doing amazing and let\'s all have a great week!')
                await asyncio.sleep(60)
            except Exception as e:
                print(e)
    elif datetime.today().weekday() == 2:
        if now_utc.hour == 12 and now_utc.minute == 0:
            try:
                channel = bot.get_channel(channel_id)
                await channel.send('It is VVibe-Check VVednesday! Are y\'all vibing today? I am!')
                await asyncio.sleep(60)
            except Exception as e:
                print(e)
    elif datetime.today().weekday() == 3:
        if now_utc.hour == 12 and now_utc.minute == 0:
            try:
                channel = bot.get_channel(channel_id)
                await channel.send('Thirsty Thursday! What are you drinking at this time? Let us know!')
                await asyncio.sleep(60)
            except Exception as e:
                print(e)

@bot.event
async def on_ready():
    print('Ready to vibe!')
    await bot.change_presence(activity=discord.Game('the vibes!'))
    timeCheck.start()


fileToken = open("token.txt", "r")
token = fileToken.read()
bot.run(token)



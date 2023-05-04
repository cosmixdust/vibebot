import aiosqlite
import asyncio
import discord
import pytz
import random

from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks

from phrases import monday, wednesday, thursday

intents = discord.Intents(
    message_content= True,
    messages= True,
    guilds= True
)

bot = commands.Bot(command_prefix='-', intents=intents)

async def send_message_to_channels(message):
    async with aiosqlite.connect('main.db') as db:
        async with db.execute('SELECT id FROM ids') as cursor:
            async for row in cursor:
                channel_id = row[0]
                channel = bot.get_partial_messageable(channel_id)
                try:
                    await channel.send(message)
                except Exception as e:
                    print(e)
            await asyncio.sleep(60)

@tasks.loop(seconds=1)
async def timeCheck():
    now_utc = datetime.now(pytz.utc)

    if all((
            now_utc.weekday() == 0,
            now_utc.hour == 12,
            now_utc.minute == 0)):
        await send_message_to_channels(random.choice(monday))

    elif all((
            now_utc.weekday() == 2,
            now_utc.hour == 12,
            now_utc.minute == 0)):
        await send_message_to_channels(random.choice(wednesday))

    elif all((
            now_utc.weekday() == 3,
            now_utc.hour == 12,
            now_utc.minute == 0)):
        await send_message_to_channels(random.choice(thursday))

@bot.event
async def on_ready():
    print('Ready to vibe!')
    await bot.change_presence(activity=discord.Game('the vibes!'))
    async with aiosqlite.connect('main.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS ids (id INTEGER, guild INTEGER)')
        await db.commit()
    timeCheck.start()
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name='set-channel', description='set a channel for vibeBot announcements (admins only).')
@app_commands.describe(channel='the channel for the announcements')
@app_commands.checks.has_permissions(administrator=True)
async def announcements(interaction: discord.Interaction, channel: discord.TextChannel):
    # Check channel is in the same guild
    if channel.guild != interaction.guild:
        return await interaction.response.send_message('That\'s not a channel on this server!', ephemeral=True)
    async with aiosqlite.connect('main.db') as db:
        cursor = await db.execute('SELECT id FROM ids WHERE guild = ?', (interaction.guild.id,))
        data = await cursor.fetchone()
        if data:
            await db.execute('UPDATE ids SET id = ? WHERE guild = ?', (channel.id, interaction.guild.id))
        else:
            await db.execute('INSERT INTO ids (id, guild) VALUES (?, ?)', (channel.id, interaction.guild.id))
        await db.commit()
    await interaction.response.send_message(f'Congrats! Your channel set for vibeBot announcements is now {channel.mention}')

@bot.tree.command(name='unsubscribe', description='unsub from announcements! (admins only)')
@app_commands.checks.has_permissions(administrator=True)
async def unsub(interaction: discord.Interaction):
    async with aiosqlite.connect('main.db') as db:
        cursor = await db.execute('SELECT id FROM ids WHERE guild = ?', (interaction.guild.id,))
        data = await cursor.fetchone()
        if data:
            await cursor.execute('DELETE FROM ids WHERE guild = ?', (int(interaction.guild.id),))
            await interaction.response.send_message('Got it! You will no longer recieve vibeBot announcements!')
        else:
            await interaction.response.send_message('You\'re not subscribed to vibeBot announcements!', ephemeral=True)
        await db.commit()

fileToken = open("token.txt", "r")
token = fileToken.read()
bot.run(token)

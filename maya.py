# bot.py

import os
import requests
import logging
from discord.ext import commands
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname) : %(name)s : %(message)s'))
logger.addHandler(handler)


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('API_URL')
KEY = os.getenv('KEY')
BID = os.getenv('BID')
API_KEY = os.getenv('API_KEY')
HOST = os.getenv('HOST')


# function call api and return json data
def getMsg(user, message):
    query = {
        "bid": BID,
        "key": KEY,
        "uid": user,
        "msg": message
    }
    headers = {
        'x-rapidapi-host': HOST,
        'x-rapidapi-key': API_KEY
    }
    response = requests.request("GET", URL, headers=headers, params=query)
    return response.json()


client = commands.Bot(command_prefix='!')


# Bot command
@client.command(pass_context=True, name='m')
async def on_help(ctx):
    await ctx.message.channel.send("Hey, I\'am here boyz, what is the problem ?")


@client.command(pass_context=True, name='mts')
async def on_translate(ctx):
    msg = getMsg(ctx.message.author, 'translate {}'.format(ctx.message.content[5:]))
    await ctx.message.channel.send(msg['cnt'])


@client.command(name='mh')
async def on_hypnosis(ctx):
    await ctx.message.channel.send('{}. Prépare toi à vivre une experience hors du commun. Dans quelque instant, '
                                   'je vais t\'hypnotiser'.format(ctx.message.author), tts=True)


@client.command(pass_context=True, name='mj')
async def on_join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command(pass_context=True, name='ml')
async def on_leave(ctx):
    await ctx.voice_client.disconnect()


# Bot event
@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send('Hi {}, welcome, say Maya if you want to talk!'.format(member.name))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'maya' in message.content.lower():
        msg = getMsg(message.author, message.content[5:])
        await message.channel.send(msg['cnt'])
    await client.process_commands(message)


client.run(TOKEN)

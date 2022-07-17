#!/usr/bin/env python3

import discord
import logging
import json
from datetime import datetime


intents = discord.Intents.all()
client = discord.Client(intents=intents)
config = {}


def get_config():
    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def update_config(new):
    global config
    with open('config.json', 'w') as f:
        json.dump(new, f, indent=4, ensure_ascii=False)


def init_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    global config

    if after.id == config['himiki_id']:
        await quote_himiki(after)


async def quote_himiki(member: discord.Member):
    global config
    global client

    if member is None or member.activity is None or member.guild.id != config['quotes_id']:
        return

    channel = client.get_channel(id=config['quotes_id'])
    status = str(member.activity)
    last_msg = config['last_msg']

    if member.activity.type != discord.ActivityType.custom or status == last_msg:
        return

    await channel.send(':red_circle: **NEW STATUS JUST DROPPED!** :red_circle:\n')
    await channel.send(f':milk: {status} :milk: ')
    config['last_msg'] = status
    config['total_msgs'] = config['total_msgs'] + 1
    update_config(config)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$summon"):
        to_summon = ' '.join(message.content.split(' ')[1:])
        await summon(to_summon, message.channel)

    elif message.content == '$mario':
        mario_gif = 'https://tenor.com/view/super-mario-mario-is-rapping-rapper-mic-gif-15160107'
        await message.channel.send(mario_gif)

    elif message.content == "$clap":
        clip = 'https://clips.twitch.tv/SassyCourteousPicklesPeteZarollTie-oEXbb-o5W7pdvuSU'
        await message.channel.send(clip)


async def summon(message, channel):
    for i in range(10):
        await channel.send(message)


def main():
    global client
    global config
    init_logger()
    config = get_config()
    client.run(config['token'])


if __name__ == '__main__':
    main()

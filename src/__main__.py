#!/usr/bin/env python3
# coding: utf-8

import discord
from os import remove, mkdir
from time import sleep
from datetime import datetime
from re import sub
from os.path import join, isdir
from os import environ
from json import loads
try:
    from .voiceroid2api import VOICEROID2
except ImportError:
    from voiceroid2api import VOICEROID2

client = discord.Client()


@client.event
async def on_ready():
    print('ログインしました')
    await client.change_presence(activity=discord.Game(name='稼働中'))


def check_error(filename):
    def wrapper(er):
        print('Error check :', er)
        sleep(1)
        remove(filename)
    return wrapper


@client.event
async def on_voice_state_update(member, before, after):
    print(before.channel, "to", after.channel)
    if after.channel is None:
        if len(before.channel.members) == 1 and before.channel.members[0].id == CONFIG["selfid"]:
            print("LEFT!")
            vc.disconnect()


@client.event
async def on_message(message):
    global vc
    global v2
    global readChannelIds
    print("MESSGAE :", message.content)
    if message.author.bot:
        return
    elif message.content.startswith("/dt"):
        commands = message.content.split()
        if commands[1] in ["s", "start"]:
            if message.author.voice is None:
                await message.channel.send("まずボイスチャンネルに接続してください")
                return
            elif len(readChannelIds) == 0:
                vc = await discord.VoiceChannel.connect(message.author.voice.channel)
            elif message.channel.id in readChannelIds:
                await message.channel.send("既にこのチャンネルの読み上げを開始しています")
                return
            readChannelIds.append(message.channel.id)
            channelsMentions = ""
            for c in readChannelIds:
                channelsMentions += "<#{}>\n".format(c)
            await message.channel.send('このチャンネルの読み上げ開始\n' + channelsMentions)
        elif commands[1] in ["e", "end"]:
            await message.channel.send('このチャンネルの読み上げ終了')
            del readChannelIds[readChannelIds.index(message.channel.id)]
            if len(readChannelIds) == 0:
                await vc.disconnect()
        elif commands[1] == "stopvoice":
            vc.stop()
        elif commands[1] == "neko":
            vc.play(discord.FFmpegPCMAudio('wagahaiwanekodearu.wav'), after=check_error)
        elif commands[1] == "test":
            pass
    elif message.content.startswith("!") or message.content.startswith("/") or message.content.startswith("?"):
        pass
    else:
        if message.channel.id not in readChannelIds:
            return
        if len(message.content) == 0:
            return
        name = message.author.nick
        if name is None:
            name = message.author
        print("Rendering \"{}\"".format(message.content))
        reading = join(CONFIG["cache"], "{}.wav".format(datetime.now().strftime("%Y%m%d%H%M%S%f")))
        renderText = name + "\n" + sub(r"[a-z]+\:\/\/[a-z.]+[^ ]*", "URL", message.content)
        v2.render(renderText, reading)
        vc.play(discord.FFmpegPCMAudio(reading), after=check_error(reading))


def main():
    global v2, CONFIG, client, readChannelIds, vc
    CONFIG_PATH = join(environ["HOMEDRIVE"], environ["HOMEPATH"], "distalkpy.json")
    CONFIG = loads(CONFIG_PATH)
    v2 = VOICEROID2()
    readChannelIds = list()
    vc = None
    if not isdir(CONFIG["cache"]):
        mkdir(CONFIG["cache"])
    client.run(CONFIG["token"])


if __name__ == '__main__':
    main()

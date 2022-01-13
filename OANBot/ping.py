import os
import sys
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from time import time
from datetime import datetime

# System Uptime
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ('Week', 60 * 60 * 24 * 7),
    ('Day', 60 * 60 * 24),
    ('Hour', 60 * 60),
    ('Min', 60),
    ('Sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(contact_filter & filters.command(['alive'], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
   start = time()
   current_time = datetime.utcnow()
   m_reply = await m.reply_text("`.....`")
   delta_ping = time() - start
   uptime_sec = (current_time - START_TIME).total_seconds()
   uptime = await _human_time_duration(int(uptime_sec))
   await m_reply.edit(f"┏━━━━━━━━━❥ \n┣✯ཧᜰ꙰ꦿ➢𝐎𝐀𝐍༒☛\n ➥ 𝐁𝐎𝐓 𝐈𝐒 𝐀𝐋𝐈𝐕𝐄[🔥](https://telegra.ph/file/bc43ae980fe2528293d45.jpg)\n┣✯**📍Ping✯⚡Pong🔊** \n ➥ `{delta_ping * 1000:.3f} ms` \n┣✯**Uptime🛎** \n➥{uptime}\n┣✯𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 \n➥[★📍𝐉𝐎𝐈𝐍📍★](https://t.me/Attitude_Network)\n┗━━━━━━━━━❥")

@Client.on_message(contact_filter & filters.command(['restart'], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
   await m.reply("𝄥𝄞─────────────\n\n 📣RESTARTING.......\n\n📍CONNECTING TO ➥𝐎𝐀𝐍༒☛ SERVER \n\n\n🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 : @Attitude_Network\n\n────────────── 𝄇")
   os.execl(sys.executable, sys.executable, *sys.argv)
   # You probably don't need it but whatever
   quit()

@Client.on_message(contact_filter & filters.command(['help'], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
   HELP = f"**⏤͟͟͞͞✯HELP MENU 🛠✰࿐** \n\n✯✯USER COMMANDS✯✯\n➠(Anyone can Use if `GROUP_MODE` is set to `True`): \n ➥ `{HNDLR}play`  \n ➥ `{HNDLR}vplay`  \n ➥ `{HNDLR}stream` (For Radio links) \n ➥ `{HNDLR}vstream` (For live video links) \n ➥ `{HNDLR}playfrom [channel] ; [n]` (Plays last n songs from channel) \n ➥ `{HNDLR}playlist`  \n ➥ `{HNDLR}queue` \n\n ✯✯SUDO COMMANDS✯✯ \n ➠(Can only be accessed by You and Your Contacts): \n ➥ `{HNDLR}alive` \n ➥ `{HNDLR}skip` \n ➥ `{HNDLR}pause` \n ➥ `{HNDLR}resume` \n ➥ `{HNDLR}stop` \n ➥ `{HNDLR}end` \n ➥ `{HNDLR}help` \n ➥ `{HNDLR}restart`"
   await m.reply(HELP)

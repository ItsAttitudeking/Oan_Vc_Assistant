import os
import asyncio
from pyrogram import Client
from OANBot.queues import QUEUE, add_to_queue
from config import bot, call_py, HNDLR, contact_filter, GRPPLAY
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped

@Client.on_message(filters.command(['playfrom'], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
 if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
   chat_id = m.chat.id
   if len(m.command) < 2:
      await m.reply("π₯πβββββββββββββ\n\nβ₯**USAGE:** \n\nβ₯`/playfrom [chat_id/username]` \nβ₯`/playfrom [chat_id/username] ; [no. of songs]`\n\nββββββββββββββ π")
   else:
      args = m.text.split(maxsplit=1)[1]
      if ";" in args:
         chat = args.split(";")[0]
         limit = int(args.split(";")[1])
      else:
         chat = args
         limit = 10
      hmm = await m.reply(f"π₯πβββββββββββββ\n\nβ₯Searching the last **{limit}** Songs from `{chat}`\n\nββββββββββββββ π")
      try:
         async for x in bot.search_messages(chat, limit=limit, filter="audio"):
               location = await x.download()
               if x.audio.title:
                  songname = x.audio.title[:30] + "..."
               else:
                  if x.audio.file_name:
                     songname = x.audio.file_name[:30] + "..."
                  else:
                     songname = "Audio"
               link = x.link
               if chat_id in QUEUE:
                  add_to_queue(chat_id, songname, location, link, "Audio", 0)
               else:
                  await call_py.join_group_call(
                     chat_id,
                     AudioPiped(
                        location
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  add_to_queue(chat_id, songname, location, link, "Audio", 0)
                  await m.reply(f"π₯πβββββββββββββ\n\nβ₯**Started Playing Songs from {chat} βΆ** \n\nβ₯**π§ SONG** : [{songname}]({link}) \n\nβ₯**π¬ CHAT** : `{chat_id}`\n\nββββββββββββββ π", disable_web_page_preview=True)
         await hmm.delete()
         await m.reply(f"Added **{limit}** SONGS to Queue")
      except Exception as e:
         await hmm.edit(f"**β₯ERRORβ οΈ**\n\nβ₯Ask to β  @OAN_Support \n\nβ₯`{e}` \n\n πππ¨π°ππ«ππ ππ² β« @Attitude_Network")

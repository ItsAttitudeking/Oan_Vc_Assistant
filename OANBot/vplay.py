import os
import re
import asyncio
from pyrogram import Client
from OANBot.queues import QUEUE, add_to_queue
from config import bot, call_py, HNDLR, contact_filter, GRPPLAY
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityAudio
from pytgcalls.types.input_stream.quality import HighQualityVideo, MediumQualityVideo, LowQualityVideo
from youtubesearchpython import VideosSearch


def ytsearch(query):
   try:
      search = VideosSearch(query, limit=1)
      for r in search.result()["result"]:
         ytid = r['id']
         if len(r['title']) > 34:
            songname = r['title'][:35] + "..."
         else:
            songname = r['title']
         url = f"https://www.youtube.com/watch?v={ytid}"
      return [songname, url]
   except Exception as e:
      print(e)
      return 0

# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
async def ytdl(link):
   proc = await asyncio.create_subprocess_exec(
       'youtube-dl',
       '-g',
       '-f',
       # CHANGE THIS BASED ON WHAT YOU WANT
       'best[height<=?720][width<=?1280]',
       f'{link}',
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE,
   )
   stdout, stderr = await proc.communicate()
   if stdout:
      return 1, stdout.decode().split('\n')[0]
   else:
      return 0, stderr.decode()


@Client.on_message(filters.command(['vplay'], prefixes=f"{HNDLR}"))
async def vplay(client, m: Message):
 if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
   replied = m.reply_to_message
   chat_id = m.chat.id
   if replied:
      if replied.video or replied.document:
         huehue = await replied.reply("`Downloading`")
         dl = await replied.download()
         link = replied.link
         if len(m.command) < 2:
            Q = 720
         else:
            pq = m.text.split(None, 1)[1]
            if pq == "720" or "480" or "360":
               Q = int(pq)
            else:
               Q = 720
               await huehue.edit("`Only 720, 480, 360 Allowed` \n`Now Streaming in 720p`")
         try:
            if replied.video:
               songname = replied.video.file_name[:35] + "..."
            elif replied.document:
               songname = replied.document.file_name[:35] + "..."       
         except:
            songname = "Video"
  
         if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
            await huehue.edit(f"┏━━━━━━━━━❥\n┣✯[〽️](https://telegra.ph/file/114b8e7116d319d231981.jpg)Queued at **#{pos}**\n┗━━━━━━━━━❥")
         else:
            if Q==720:
               hmmm = HighQualityVideo()
            elif Q==480:
               hmmm = MediumQualityVideo()
            elif Q==360:
               hmmm = LowQualityVideo()
            await call_py.join_group_call(
               chat_id,
               AudioVideoPiped(
                  dl,
                  HighQualityAudio(),
                  hmmm
               ),
               stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, link, "Video", Q)
            await huehue.edit(f"┏━━━━━━━━━❥\n✯✯**Started Playing Video ▶**✯✯ \n┣✯**🎧SONG** : [{songname}]({link}) \n┣✯**💬 CHAT** : `{chat_id}`\n┣✯🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 : @Attitude_Network\n┗━━━━━━━━━❥", disable_web_page_preview=True)
      else:
         if len(m.command) < 2:
            await m.reply("𝄥𝄞─────────────\n\n➥Reply to an Audio File or give something to Search\n\n────────────── 𝄇")
         else:
            huehue = await m.reply("🔎")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search==0:
               await huehue.edit("𝄥𝄞─────────────\n\n➥Found Nothing for the Given Query.\n\n────────────── 𝄇")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{ytlink}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                     await huehue.edit(f"┏━━━━━━━━━❥\n┣✯[〽️](https://telegra.ph/file/114b8e7116d319d231981.jpg)Queued at **#{pos}**\n┗━━━━━━━━━❥")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                              ytlink,
                              HighQualityAudio(),
                              hmmm
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.edit(f"┏━━━━━━━━━❥\n┣✯**Started Playing Video ▶**\n┣✯**🎧SONG** : [{songname}]({link}) \n┣✯**💬 CHAT** : `{chat_id}` \n┣✯𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➠ @Attitude_Network\n┗━━━━━━━━━❥", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")
            
   else:
         if len(m.command) < 2:
            await m.reply("`Reply to an Audio File or give something to Search`")
         else:
            huehue = await m.reply("`Searching...`")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search==0:
               await huehue.edit("𝄥𝄞─────────────\n\n ⏤͟͟͞͞✯Found Nothing for the Given Query\n\n────────────── 𝄇")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{ytlink}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                     await huehue.edit(f"┏━━━━━━━━━❥\n┣✯[〽️](https://telegra.ph/file/114b8e7116d319d231981.jpg)Queued at **#{pos}**\n┗━━━━━━━━━❥")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                              ytlink,
                              HighQualityAudio(),
                              hmmm
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.edit(f"┏━━━━━━━━━❥\n┣✯**Started Playing Video ▶**\n┣✯**🎧SONG** : [{songname}]({link}) \n┣✯**💬 CHAT** : `{chat_id}` \n┣✯𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➠ @Attitude_Network\n┗━━━━━━━━━❥", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(['vstream'], prefixes=f"{HNDLR}"))
async def vstream(client, m: Message):
 if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
   chat_id = m.chat.id
   if len(m.command) < 2:
      await m.reply("`Give A Link/LiveLink/.m3u8 URL/YTLink to Stream from 🎶`")
   else:
      if len(m.command)==2:
         link = m.text.split(None, 1)[1]
         Q = 720
         huehue = await m.reply("𝄥𝄞─────────────\n\n➥Trying to Stream 💭\n\n────────────── 𝄇")
      elif len(m.command)==3:
         op = m.text.split(None, 1)[1]
         link = op.split(None, 1)[0]
         quality = op.split(None, 1)[1]
         if quality == "720" or "480" or "360":
            Q = int(quality)
         else:
            Q = 720
            await m.reply("`Only 720, 480, 360 Allowed` \n`Now Streaming in 720p`")
         huehue = await m.reply("𝄥𝄞─────────────\n\n➥Trying to Stream 💭\n\n────────────── 𝄇")
      else:
         await m.reply("`!vstream {link} {720/480/360}`")

      # Filtering out YouTube URL's
      regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
      match = re.match(regex,link)
      if match:
         hm, livelink = await ytdl(link)
      else:
         livelink = link
         hm = 1

      if hm==0:
         await huehue.edit(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{ytlink}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
      else:
         if chat_id in QUEUE:
            pos = add_to_queue(chat_id, "Live Stream 📺", livelink, link, "Video", Q)
            await huehue.edit(f"┏━━━━━━━━━❥\n┣✯[〽️](https://telegra.ph/file/114b8e7116d319d231981.jpg)Queued at **#{pos}**\n┗━━━━━━━━━❥")
         else:
            if Q==720:
               hmmm = HighQualityVideo()
            elif Q==480:
               hmmm = MediumQualityVideo()
            elif Q==360:
               hmmm = LowQualityVideo()
            try:
               await call_py.join_group_call(
                  chat_id,
                  AudioVideoPiped(
                     livelink,
                     HighQualityAudio(),
                     hmmm
                  ),
                  stream_type=StreamType().pulse_stream,
               )
               add_to_queue(chat_id, "Live Stream 📺", livelink, link, "Video", Q)
               await huehue.edit(f"┏━━━━━━━━━❥\n┣✯**Started Playing Audio [▶](https://telegra.ph/file/114b8e7116d319d231981.jpg)**\n┃\n┣✯**🎧** ➫ **[Live Stream 📺]({link})** \n┣✯**💬 CHAT** : `{chat_id}` \n┃\n┣✯𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➠ @Attitude_Network\n┗━━━━━━━━━❥", disable_web_page_preview=True)
            except Exception as ep:
               await huehue.edit(f"`{ep}`")

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from OANBot.handlers import skip_current_song, skip_item
from OANBot.queues import QUEUE, clear_queue

@Client.on_message(contact_filter & filters.command(['skip'], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
   chat_id = m.chat.id
   if len(m.command) < 2:
      op = await skip_current_song(chat_id)
      if op==0:
         await m.reply("𝄥𝄞─────────────\n\n➥Nothing Is Playing\n\n────────────── 𝄇")
      elif op==1:
         await m.reply("𝄥𝄞─────────────\n\n➥Queue is Empty, Leaving Voice Chat...\n\n────────────── 𝄇")
      elif op==2:
         await m.reply(f"𝄥𝄞─────────────\n\n➥ ⚠️**Some Error Occurred**⚠️ \n\n➥`Clearing the Queues and Leaving the Voice Chat...`\n\n────────────── 𝄇")
      else:
         await m.reply(f"𝄥𝄞─────────────\n\n✯✯**Skipped ⏭**✯✯ \n\n➥**🎧 Now Playing** ➫ [{op[0]}]({op[1]}) | `{op[2]}` \n\n➥🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 : @Attitude_Network\n\n────────────── 𝄇", disable_web_page_preview=True)
   else:
      skip = m.text.split(None, 1)[1]
      OP = "𝄥𝄞─────────────\n\n➥**Removed the following songs from Queue:-**"
      if chat_id in QUEUE:
         items = [int(x) for x in skip.split(" ") if x.isdigit()]
         items.sort(reverse=True)
         for x in items:
            if x==0:
               pass
            else:
               hm = await skip_item(chat_id, x)
               if hm==0:
                  pass
               else:
                  OP = OP + "\n" + f"**#{x}** - {hm}"
         await m.reply(OP)        
      
@Client.on_message(contact_filter & filters.command(['end', 'stop'], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         await m.reply("𝄥𝄞─────────────\n\n➥**Stopped Streaming ⏹️**\n\n────────────── 𝄇")
      except Exception as e:
         await m.reply(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{e}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
   else:
      await m.reply("𝄥𝄞─────────────\n\n➥Nothing is Streaming.\n\n────────────── 𝄇")
   
@Client.on_message(contact_filter & filters.command(['pause'], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.pause_stream(chat_id)
         await m.reply("𝄥𝄞─────────────\n\n➥**Paused Streaming ⏸️**\n\n────────────── 𝄇")
      except Exception as e:
         await m.reply(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{e}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
   else:
      await m.reply("𝄥𝄞─────────────\n\n➥Nothing is Streaming\n\n────────────── 𝄇")
      
@Client.on_message(contact_filter & filters.command(['resume'], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.resume_stream(chat_id)
         await m.reply("𝄥𝄞─────────────\n\n➥**Resumed Streaming ▶**\n\n────────────── 𝄇")
      except Exception as e:
         await m.reply(f"**➥ERROR⚠️**\n\n➥Ask to ➠ @OAN_Support \n\n➥`{e}` \n\n 🔗𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 ➫ @Attitude_Network")
   else:
      await m.reply("𝄥𝄞─────────────\n\n➥Nothing is Streaming\n\n────────────── 𝄇")

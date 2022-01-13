from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from OANBot.queues import QUEUE, get_queue
from config import HNDLR, contact_filter, GRPPLAY

@Client.on_message(filters.command(['playlist', 'queue'], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
 if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
   chat_id = m.chat.id
   if chat_id in QUEUE:
      chat_queue = get_queue(chat_id)
      if len(chat_queue)==1:
         await m.reply(f"𝄥𝄞─────────────\n\n✯✯**[🎧](https://telegra.ph/file/114b8e7116d319d231981.jpg)NOW PLAYING:**✯✯ \n\n➥[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`\n\n────────────── 𝄇", disable_web_page_preview=True)
      else:
         QUE = f"**𝄥𝄞─────────────\n\n✯✯[🎧](https://telegra.ph/file/114b8e7116d319d231981.jpg)NOW PLAYING:**✯✯ \n\n➥[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n✯✯**⏯ PLAYLIST:**✯✯"
         l = len(chat_queue)
         for x in range (1, l):
            hmm = chat_queue[x][0]
            hmmm = chat_queue[x][2]
            hmmmm = chat_queue[x][3]
            QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
         await m.reply(QUE, disable_web_page_preview=True)
   else:
      await m.reply("𝄥𝄞─────────────\n\n➥Nothing is Streaming🔊\n\n────────────── 𝄇")

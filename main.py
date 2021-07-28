import discord
import os
import asyncio
import datetime
import re
from random import randrange
from replit import db 
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return
    
    text = message.content.split()
    user = 0

    if len(text) >= 2:
      user = text[1]
    
    if text[0] == '!addpizza' and len(text) == 2:
      if user.lower() in db:
        db[user.lower()].append(str(message.created_at.date()))
      else:
        db[user.lower()] = [str(message.created_at.date())]
      await message.channel.send(f"{user} hat schon {len(db[user.lower()])} mal Pizza gegessen. Penner!")
      await message.delete()

    elif text[0] == '!addpizza' and len(text) == 3 and re.match("202[0-9]-[0-1][0-9]-[0-3][0-9]", text[2]):
      if user.lower() in db:
        db[user.lower()].append(text[2])
      else:
        db[user.lower()] = [text[2]]
      await message.channel.send(f"{user} hat schon {len(db[user.lower()])} mal Pizza gegessen. Penner!")
      await message.delete()

    elif text[0] == '!getpizza' and len(text) == 2:
      await message.channel.send(f"{user} hat schon {len(db[user.lower()])} mal Pizza gegessen. Penner!")
      await message.delete()

    elif text[0] == '!getpizza' and len(text) == 3:
      count = 0
      datetoday = datetime.date.today()
      for i in db[user.lower()]:
        iDate = datetime.datetime.strptime(i, "%Y-%m-%d").date()
        if (datetoday - iDate).days <= int(text[2]):
          count += 1
        else: break
      await message.channel.send(f"{user} hat in den letzten {text[2]} Tagen {count} mal Pizza gegessen.")
      await message.delete()

    elif text[0] == '!getpizzadates' and len(text) == 2:
      await message.channel.send(f"{user}: {', '.join(db[user.lower()])}")
      await message.delete()

    elif text[0] == '!resetpizza' and message.author.id == int(os.environ['myID']):
      db[user.lower()] = []
      await message.channel.send(f"{user}`s Pizzaspeicher wurde gelöscht")
      await message.delete()

    elif text[0] == '!substractpizza' and message.author.id == int(os.environ['myID']):
      db[user.lower()] = text[2]
      for i in range(text[2]):
        pass
      await message.channel.send(f"{user} hat schon {db[user.lower()]} mal Pizza gegessen. Penner!")
      await message.delete()

    elif text[0] == '!getallpizza' and len(text) == 1:
      liste = ""
      for i in db.keys():
        liste += (str(i) + ": " + str(len(db[i])) + "\n")
      await message.channel.send(liste)
      await message.delete()

    elif text[0] == '!helppizza':
      await message.channel.send("!addpizza user [year-month-day]: fügt gegessene Pizza für user heute [oder eingetragenes Datum] ein \n!getpizza user [int]: gibt gegessene Pizzen für user zurück [begrenzt auf die letzten int tage] \n!getpizzadates user: gibt die Daten des Pizzaessens für user aus\n!getallpizza: gibt alle einträge aus\n!addquotepizza: fügt ein Zitat hinzu\n!quotepizza: gibt ein zufälliges zitat aus\n Lustige neue Ideen sind gerne gesehen")
      await message.delete()

    elif text[0] == '!deletepizza' and message.author.id == int(os.environ['myID']):
      if db[user]:
        del db[user]
      await message.channel.send(f"{user} wurde gelöscht")
      await message.delete()
    
    elif text[0] == '!deleteallpizzayesimsure' and message.author.id == int(os.environ['myID']):
      for i in db.keys():
        del db[i]
      await message.channel.send(f"keys: {''.join(db.keys())}")
      await message.delete()

    elif text[0] == '!quotepizza':
      if db["quotes"]:
        i = randrange(len(db["quotes"]))
        quote = db["quotes"][i]
        await message.channel.send(f"{quote}")
      else:
        await message.channel.send(f"keine Zitate vorhanden")
      await message.delete()
    
    elif text[0] == '!addquotepizza':
      if len(text) > 1:
        del text[0]
        if "quotes" in db:
          db["quotes"].append(" ".join(text))
        else:
          db["quotes"] = [" ".join(text)]
        await message.channel.send(f"Zitat: '{' '.join(text)}' wurde hinzugefügt")
      else: 
        await message.channel.send(f"kein Text eingegeben")
      await message.delete()
    
    elif text[0] == '!getquotespizza' and message.author.id == int(os.environ['myID']):
      qlist = []
      for i in range(len(db["quotes"])):
        qlist.append(str(i))
        qlist.append(db["quotes"][i])
      await message.channel.send(f"Zitate: {' '.join(qlist)}")
      await message.delete()

    elif text[0] == '!delquotepizza' and message.author.id == int(os.environ['myID']):
      quote = db["quotes"][int(text[1])]
      del db["quotes"][int(text[1])]
      await message.channel.send(f"Zitat: '{quote}' wurde gelöscht")
      await message.delete()
    
    elif text[0].startswith("!") and "pizza" in text[0]:
      reply = await message.channel.send(f"{message.content} ist kein gültiger Befehl für den Pizzabot. (falls diese Nachricht nicht für den Pizzabot war tut es mir leid")
      await asyncio.sleep(10)
      await reply.delete()

keep_alive()
client.run(os.environ['TOKEN'])


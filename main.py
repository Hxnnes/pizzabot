import discord
import os
from replit import db 
from keep_alive import keep_alive

client = discord.Client()

def update_user(user):
  if user in db.keys():
    db[user] = db[user] + 1
  else:
    db[user] = 1

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content
    text = msg.split()
    user = 0
    if len(text) >= 2:
      user = text[1]
    
    if msg.startswith('!addpizza'):
      update_user(user.lower())
      await message.channel.send(f"{user} hat schon {db[user.lower()]} mal Pizza gegessen. Penner!")

    if msg.startswith('!getpizza'):
      await message.channel.send(f"{user} hat schon {db[user.lower()]} mal Pizza gegessen. Penner!")

    if msg.startswith('!resetpizza'):
      db[user.lower()] = 0
      await message.channel.send(f"{user}`s Pizzaspeicher wurde gelöscht")

    if msg.startswith('!setpizza'):
      db[user.lower()] = text[2]
      await message.channel.send(f"{user} hat schon {db[user.lower()]} mal Pizza gegessen. Penner!")

    if msg.startswith('!getallpizza'):
      liste = ""
      for i in db.keys():
        liste += (str(i) + ": " + str(db[i]) + "\n")
      await message.channel.send(liste)

    if msg.startswith('!helppizza'):
      await message.channel.send("!addpizza user: erhöht Pizzazähler für user \n!getpizza user: gibt den Pizzazähler für user zurück \n!resetpizza user: setzt Pizzazähler für user zurück \n!setpizza user integer: setzt den Pizazähler von user auf den integer\n!getallpizza: gibt alle einträge aus\n Lustige neue Ideen sind gerne gesehen")

    if msg.startswith('!deletepizza') and str(message.author) =="Hxnnes#3925":
      del db[user]
      await message.channel.send(f"{user} wurde gelöscht")

    if msg.startswith('!deleteallpizzayesimsure') and str(message.author) =="Hxnnes#3925":
      for i in db.keys():
        del db[i]
      await message.channel.send(f"keys: {''.join(db.keys())}")

keep_alive()
client.run(os.getenv('TOKEN'))

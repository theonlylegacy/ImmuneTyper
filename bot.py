import discord
import json
import time
import os

with open("Config.json") as file:
    bot_config = json.load(file)
    bot_token = bot_config.get("token")

def capitalize(string):
    words = []
    extensions = (".txt", ".jpg", ".png", ".lua")

    for word in string.split():
        if word and word.startswith(("http://", "https://", "www.")):
            words.append(word)
        elif word and word.endswith(extensions):
            words.append(word)
        elif word:
            capitalized = word[0].upper() + word[1:]
            words.append(capitalized)

    return " ".join(words)

class bot_init(discord.Client):
    async def on_ready(self):
        print(f"{self.user} detected")
            
    async def on_message(self, message):
        if message.author.id == self.user.id:
            await message.edit(capitalize(message.content))

bot_client = bot_init()
bot_client.run(bot_token)

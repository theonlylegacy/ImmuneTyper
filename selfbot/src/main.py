import discord
import os
from re import findall
from base64 import b64decode
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from json import loads

discord_path = os.path.expandvars(r"%userprofile%\Appdata\Roaming\discord\Local Storage\leveldb")

if not os.path.exists(discord_path):
    os._exit(9)

# Discord uses AES encryption for their tokens
def decrypt(buff, key):
    try:
        return AES.new(CryptUnprotectData(key)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "error"

# Discord stores tokens in their log files
def get_token():
    token = None
    
    for name in os.listdir(discord_path):
        with open(os.path.expandvars(r"%userprofile%\AppData\Roaming\discord\Local State"), "r", errors="ignore") as file:
            key = loads(file.read())["os_crypt"]["encrypted_key"]
            file.close()
        
        if name.endswith(".log") or name.endswith(".ldb"):
            for line in [x.strip() for x in open(f"{discord_path}\\{name}", errors = "ignore").readlines() if x.strip()]:
                for token in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    token = decrypt(b64decode(token.split("dQw4w9WgXcQ:")[1]), b64decode(key)[5:])
                    break
    return token


def capitalize(string, seperator):
    output = []
    links = ("http://", "https://", "www.")
    extensions = (".txt", ".jpg", ".png", ".lua") # This doesn't support all extensions and there's probably a better way around this
    lines = string.splitlines(keepends = True)
    
    for line in lines:
        capitalized_line = []
        split_line = line.split(seperator)
        
        for i, word in enumerate(split_line):
            if word and word.startswith(links):
                capitalized_line.append(word)
            elif word and word.endswith(extensions):
                capitalized_line.append(word)
            elif word:
                capitalized = word[0].upper() + word[1:]
                capitalized_line.append(capitalized)

            if i < len(split_line) - 1:
                capitalized_line.append(seperator)

        output.append(("").join(capitalized_line))

    return ("").join(output)
        
class bot_init(discord.Client):
    async def on_ready(self):
        print(f"{self.user} connected")
            
    async def on_message(self, message):
        if message.author.id == self.user.id:
            content = message.content

            # Don't hate on this banger code

            capitalized = capitalize(message.content, " ")
            capitalized = capitalize(capitalized, "_")
            capitalized = capitalize(capitalized, "-")
            capitalized = capitalize(capitalized, "\"")
            capitalized = capitalize(capitalized, "(")
            capitalized = capitalize(capitalized, ")")

            if content != capitalized:
                await message.edit(capitalized)
                
bot_token = get_token()
        
if bot_token:
    bot_client = bot_init()
    bot_client.run(bot_token)

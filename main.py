import os
from dotenv import load_dotenv
load_dotenv()
import discord as dc
from discord.ext import commands as cmd
from discord import app_commands as appcmd
import random
import asyncio

"""
on_ready() — Runs when the bot successfully connects to Discord

on_message(message) — Runs whenever a message is sent in a channel the bot can see
on_message_edit(before, after) — Runs when a message is edited
on_message_delete(message) — Runs when a message is deleted

on_member_join(member) — Runs when a user joins the server
on_member_remove(member) — Runs when a user leaves or is kicked from the server
on_member_update(before, after) — Runs when a member's info changes (roles, nickname, etc.)

on_guild_join(guild) — Runs when the bot joins a new server
on_guild_remove(guild) — Runs when the bot is removed from a server

on_reaction_add(reaction, user) — Runs when someone adds a reaction to a message
on_reaction_remove(reaction, user) — Runs when someone removes a reaction from a message
"""

class Client(cmd.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        self.admin = "initys_imran"

        try:
            guild = dc.Object(id=1480955922770821122)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f"Error while syncing: {e}")

    async def on_message(self, message):

        if message.author == self.user:
            print(f'I sent the message: {message.content}')
            return

        print(f'Message from {message.author}: {message.content}')

        if message.content.lower().startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')

        if message.content.lower().startswith('bot sag '):
            await message.channel.send(f'{message.content[8:]}')

        if message.content.lower() == 'bot, aus' and message.author == self.admin:
            await message.channel.send('Tschüss! 👋')
            await self.close()

        await self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f'You reacted with {reaction}')


intents = dc.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = dc.Object(id=1480955922770821122)

# '/' COMMANDS
@client.tree.command(name="greet", description="sagt Hallo", guild=GUILD_ID)
async def greet(interaction: dc.Interaction):
    await interaction.response.send_message("Hallo!")

@client.tree.command(name="sag", description="sagt was du wilst", guild=GUILD_ID)
async def say(interaction: dc.Interaction, nachricht: str):
    await interaction.response.send_message(f"{nachricht}")

@client.tree.command(name="werbung", description="DEMO", guild=GUILD_ID)
async def Embed(interaction: dc.Interaction): #     
    TemuAdd = dc.Embed(title="Beste Tablette", 
                     description="Das ist in Temu aber Kopf hoch!", 
                     url="https://www.temu.com/de/xiaomi--pad-2-wifi-4gb-128gb-8gb-256gb--helio--ultra-11-90-hz-ruckkamera-8-mp-9000-mah-xiaomi--2-ladegerat-nicht-enthalten-modell-25040rp0ae-g-603940749999736.html?_oak_mp_inf=EPj8%2Bc7%2BqIkBGiBkZTgxMGExMmZjZDU0M2JhYmQyNTkxY2ExODBiYWI4NSDHmLHszTM%3D&top_gallery_url=https%3A%2F%2Fimg-eu.kwcdn.com%2Flocal-goods-img%2F212a0c9a08%2F3a8d8266-185b-4ce3-9c47-37c78d70080e_800x800.png&spec_gallery_id=33793633131&refer_page_sn=10009&freesia_scene=2&_oak_freesia_scene=2&_oak_rec_ext_1=MTI2OTk&_oak_gallery_order=1190394804&search_key=taplet&refer_page_el_sn=200049&_x_sessn_id=y6dqwqp59s&refer_page_name=search_result&refer_page_id=10009_1773243486284_6fpy05msox",
                         color=dc.Color.orange())
    TemuAdd.set_thumbnail(url="https://img-eu.kwcdn.com/local-goods-img/212a0c9a08/3a8d8266-185b-4ce3-9c47-37c78d70080e_800x800.png?imageView2/2/w/800/q/70/format/avif")
    TemuAdd.add_field(name="Es lohnt sich", value="Es ist halt Temu!!")

    await interaction.response.send_message(embed=TemuAdd)

@client.tree.command(name="wurfel", description="würfel", guild=GUILD_ID)
async def wurfel(interaction: dc.Interaction, seiten: int):
    await interaction.response.send_message("🎲 Würfeln...")
    
    for _ in range(5):
        await asyncio.sleep(0.1)
        await interaction.edit_original_response(content=f"🎲 {random.randint(1, seiten)}")
    
    finale = random.randint(1, seiten)
    await asyncio.sleep(0.1)
    await interaction.edit_original_response(content=f"🎲 Finale Nummer mit {seiten} Seiten = **{finale}**")

client.run(os.getenv("TOKEN"))

import os
from dotenv import load_dotenv
load_dotenv()

import discord as dc
from discord.ext import commands as cmd
from discord import app_commands as appcmd
import random
import asyncio

class Client(cmd.Bot):

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        try:
            guild = dc.Object(id=1480955922770821122)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to {guild.id}")
        except Exception as e:
            print(e)

    async def on_message(self, message):

        if message.author == self.user:
            return

        print(f"{message.author}: {message.content}")

        if message.content.lower().startswith("hello"):
            await message.channel.send(f"Hi {message.author} 👋")

        if message.content.lower().startswith("bot sag "):
            await message.channel.send(message.content[8:])

        await self.process_commands(message)

    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"👋 Willkommen {member.mention} auf dem Server!")

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        await reaction.message.channel.send(f"{user} reacted with {reaction.emoji}")


intents = dc.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix="!", intents=intents)

GUILD_ID = dc.Object(id=1480955922770821122)

# ---------------- SLASH COMMANDS ----------------

@client.tree.command(name="greet", description="sagt Hallo", guild=GUILD_ID)
async def greet(interaction: dc.Interaction):
    await interaction.response.send_message("Hallo! 👋")


@client.tree.command(name="sag", description="bot sagt etwas", guild=GUILD_ID)
async def say(interaction: dc.Interaction, nachricht: str):
    await interaction.response.send_message(nachricht)


@client.tree.command(name="ping", description="zeigt bot ping", guild=GUILD_ID)
async def ping(interaction: dc.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! {latency}ms")


@client.tree.command(name="random", description="zufällige zahl", guild=GUILD_ID)
async def random_number(interaction: dc.Interaction, min: int, max: int):
    number = random.randint(min, max)
    await interaction.response.send_message(f"🎲 Zufallszahl: **{number}**")


@client.tree.command(name="wurfel", description="würfel", guild=GUILD_ID)
async def wurfel(interaction: dc.Interaction, seiten: int):

    await interaction.response.send_message("🎲 Würfeln...")

    for _ in range(5):
        await asyncio.sleep(0.15)
        await interaction.edit_original_response(
            content=f"🎲 {random.randint(1, seiten)}"
        )

    finale = random.randint(1, seiten)
    await asyncio.sleep(0.15)

    await interaction.edit_original_response(
        content=f"🎲 Finale Nummer mit {seiten} Seiten = **{finale}**"
    )


@client.tree.command(name="rps", description="Schere Stein Papier", guild=GUILD_ID)
async def rps(interaction: dc.Interaction, choice: str):

    options = ["stein", "papier", "schere"]
    bot = random.choice(options)

    if choice not in options:
        await interaction.response.send_message(
            "Bitte wähle: stein, papier oder schere"
        )
        return

    if choice == bot:
        result = "Unentschieden 🤝"
    elif (
        (choice == "stein" and bot == "schere") or
        (choice == "papier" and bot == "stein") or
        (choice == "schere" and bot == "papier")
    ):
        result = "Du gewinnst! 🎉"
    else:
        result = "Ich gewinne 😎"

    await interaction.response.send_message(
        f"Du: **{choice}**\nBot: **{bot}**\n{result}"
    )


@client.tree.command(name="werbung", description="Embed Demo", guild=GUILD_ID)
async def werbung(interaction: dc.Interaction):

    embed = dc.Embed(
        title="Beste Tablette",
        description="Das ist in Temu aber Kopf hoch!",
        url="https://temu.com",
        color=dc.Color.orange()
    )

    embed.set_thumbnail(
        url="https://img-eu.kwcdn.com/local-goods-img/212a0c9a08/3a8d8266-185b-4ce3-9c47-37c78d70080e_800x800.png"
    )

    embed.add_field(
        name="Es lohnt sich",
        value="Es ist halt Temu!!"
    )

    await interaction.response.send_message(embed=embed)


# ---------------- MODERATION ----------------

@client.tree.command(name="kick", description="kicke ein Mitglied", guild=GUILD_ID)
@appcmd.checks.has_permissions(kick_members=True)
async def kick(
        interaction: dc.Interaction,
        member: dc.Member,
        reason: str = "Kein Grund"
):
    await member.kick(reason=reason)

    await interaction.response.send_message(
        f"👢 {member} wurde gekickt. Grund: {reason}"
    )


@client.tree.command(name="clear", description="löscht Nachrichten", guild=GUILD_ID)
@appcmd.checks.has_permissions(manage_messages=True)
async def clear(interaction: dc.Interaction, amount: int):

    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(limit=amount)

    await interaction.followup.send(
        f"🧹 {len(deleted)} Nachrichten gelöscht",
        ephemeral=True
    )


@client.tree.command(name="botinfo", description="info über den bot", guild=GUILD_ID)
async def botinfo(interaction: dc.Interaction):

    embed = dc.Embed(
        title="🤖 Bot Info",
        description="Python Discord Bot",
        color=dc.Color.blue()
    )

    embed.add_field(name="Server", value=len(client.guilds))
    embed.add_field(name="Ping", value=f"{round(client.latency*1000)}ms")

    embed.set_footer(text="Powered by discord.py")

    await interaction.response.send_message(embed=embed)


client.run(os.getenv("TOKEN"))
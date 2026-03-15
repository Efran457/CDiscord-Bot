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

        if message.content.lower().startswith("bot stop"):
            await message.channel.send("Bye")
            await self.close()

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

#ExtraClasses
class SimpleButton(dc.ui.Button):

    def __init__(self, label, style, callback_func=None):
        super().__init__(label=label, style=style)
        self.callback_func = callback_func

    async def callback(self, interaction: dc.Interaction):

        if self.callback_func:
            await self.callback_func(interaction, self)

class ButtonView(dc.ui.View):

    def __init__(self, buttons: list):
        super().__init__(timeout=60)

        for button in buttons:
            self.add_item(button)


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
async def rps(interaction: dc.Interaction):

    options = ["stein", "papier", "schere"]

    async def play(interaction: dc.Interaction, button):

        player = button.label.split(" ")[1].lower()
        bot = random.choice(options)

        if player == bot:
            result = "Unentschieden 🤝"
        elif (
            (player == "stein" and bot == "schere") or
            (player == "papier" and bot == "stein") or
            (player == "schere" and bot == "papier")
        ):
            result = "Du gewinnst! 🎉"
        else:
            result = "Ich gewinne 😎"

        await interaction.response.edit_message(
            content=f"Du: **{player}**\nBot: **{bot}**\n{result}",
            view=None
        )

    buttons = [
        SimpleButton("🪨 Stein", dc.ButtonStyle.primary, play),
        SimpleButton("📄 Papier", dc.ButtonStyle.success, play),
        SimpleButton("✂️ Schere", dc.ButtonStyle.danger, play)
    ]

    view = ButtonView(buttons)

    await interaction.response.send_message(
        "🎮 **Schere Stein Papier**\nWähle deine Option:",
        view=view
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

@client.tree.command(name="help", description="zeigt alle bot commands", guild=GUILD_ID)
async def help_command(interaction: dc.Interaction):

    embed = dc.Embed(
        title="🤖 Bot Commands",
        description="Hier sind alle verfügbaren Commands:",
        color=dc.Color.green()
    )

    embed.add_field(
        name="👋 Allgemein",
        value="""
/greet – sagt Hallo
/sag – bot sagt deine Nachricht
/ping – zeigt bot ping
/info – zeigt bot info
""",
        inline=False
    )

    embed.add_field(
        name="🎲 Fun",
        value="""
/random – zufällige Zahl
/wurfel – würfeln
/rps – Schere Stein Papier
""",
        inline=False
    )

    embed.add_field(
        name="🔧 Moderation",
        value="""
/kick – kickt ein Mitglied
/clear – löscht Nachrichten
""",
        inline=False
    )

    embed.add_field(
        name="📢 Sonstiges",
        value="""
/werbung – Embed Demo
/help – zeigt diese Liste
""",
        inline=False
    )

    embed.set_footer(text="Cockie Bot")

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="buttons", description="test buttons", guild=GUILD_ID)
async def buttons(interaction: dc.Interaction):

    buttons = [
        SimpleButton("🔴 Red", dc.ButtonStyle.danger),
        SimpleButton("🟢 Green", dc.ButtonStyle.success),
        SimpleButton("🔵 Blue", dc.ButtonStyle.primary)
    ]

    view = ButtonView(buttons)

    await interaction.response.send_message(
        "Click a button:",
        view=view
    )

client.run(os.getenv("TOKEN"))

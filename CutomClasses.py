import discord as dc
class SimpleButton(dc.ui.Button):

    def __init__(self, label, style, custom_id=None):
        super().__init__(label=label, style=style, custom_id=custom_id)

    async def callback(self, interaction: dc.Interaction):
        await interaction.response.send_message(
            f"You pressed **{self.label}**",
            ephemeral=True
        )
class ButtonView(dc.ui.View):

    def __init__(self, buttons: list):
        super().__init__(timeout=60)

        for button in buttons:
            self.add_item(button)

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
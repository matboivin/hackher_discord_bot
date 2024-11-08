"""Command callback for help command."""

from discord import Colour, Embed, Interaction

from .formatting import log_interaction


async def help(interaction: Interaction) -> None:
    """Display all available commands.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).

    """
    log_interaction(interaction)
    usage_message = Embed(title="HELP 🤖", colour=Colour.purple())

    usage_message.add_field(
        name="**🇬🇧 AVAILABLE COMMANDS**",
        value=(
            "Chatbot's messages will disappear after a few seconds "
            "(it can take 20 to 60 sec depending on the command used)."
        ),
        inline=False,
    )
    usage_message.add_field(
        name="**/add_resource**",
        value="*Index a resource's link.*",
        inline=False,
    )
    usage_message.add_field(
        name="**/get_resources**",
        value="*Display all resources or only those matching category.*",
        inline=False,
    )

    usage_message.add_field(
        name="**🇫🇷 COMMANDES DISPONIBLES**",
        value=(
            "*Les messages de Chatbot disparaissent après quelques secondes "
            "(après 20 à 60 sec selon les commandes).*"
        ),
        inline=False,
    )
    usage_message.add_field(
        name="**/add_resource**",
        value="*Enregistre le lien d'une ressource.*",
        inline=False,
    )
    usage_message.add_field(
        name="**/get_resources**",
        value="*Affiche toutes les ressources ou la catégorie sélectionnée.*",
        inline=False,
    )

    await interaction.response.send_message(
        embed=usage_message, ephemeral=True, delete_after=60.0
    )

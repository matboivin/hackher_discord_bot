"""Command callbacks for resources."""

from discord import Embed, Interaction
from discord.app_commands import Choice, choices, describe
from discord.app_commands.errors import CommandInvokeError

from chatbot.classes import CATEGORIES
from chatbot.database import (
    create_resource,
    fetch_all_resources,
    fetch_category,
    fetch_resources,
)
from chatbot.logger import programLogger

from .formatting import create_response, log_bot_action, log_interaction


@describe(url="The link starting with 'http(s)://'")
@describe(category="The category")
@choices(category=CATEGORIES)
async def add_resource(
    interaction: Interaction, url: str, category: Choice[str]
) -> None:
    """Index a resource's link.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).
    url : str
        The URL to add.
    category : discord.app_commands.Choice
        The URL's category.

    """
    action: str = log_interaction(interaction)

    try:
        response: Embed | None = None

        if not url or not (
            url.startswith("http://") or url.startswith("https://")
        ):
            response = create_response(
                "Please provide a link starting with 'http(s)://'.",
                type="error",
            )
            await log_bot_action(f"{action} Wrong URL: '{url}'")

        else:
            if create_resource(url, category.value):
                response = create_response(
                    f"Link added to {category.name} category.",
                    type="success",
                )

            else:
                response = create_response(
                    "Error. Please contact administrator.", type="error"
                )
                await log_bot_action(f"{action} Database error.")

    except ValueError as err:
        response = create_response(str(err), type="error")

    except CommandInvokeError as err:
        programLogger.error(err)
        response = create_response("Wrong command.", type="error")
        await log_bot_action(f"{action} Wrong command.")

    await interaction.response.send_message(
        embed=response, ephemeral=True, delete_after=20.0
    )


async def get_all_resources(interaction: Interaction) -> None:
    """Display all resources.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).

    """
    resources: dict[str, list[str]] = fetch_all_resources()

    if resources:
        link_list: str = ""

        for category_id, links in resources.items():
            category_list: str = "\n".join(set(links))
            link_list += (
                f"**{fetch_category(category_id)}**\n{category_list}\n"
            )

        await interaction.response.send_message(
            embed=create_response(link_list, type="success"),
            ephemeral=True,
            delete_after=60.0,
        )

    else:
        await interaction.response.send_message(
            embed=create_response(
                f"🇬🇧 No resources found.\n🇫🇷 Aucune ressource trouvée.",
                type="warning",
            ),
            ephemeral=True,
            delete_after=20.0,
        )


async def get_category_resources(
    interaction: Interaction, category: Choice[str]
) -> None:
    """Display all resources matching category.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).
    category : discord.app_commands.Choice
        The category to display.

    """
    resources: list[str] = fetch_resources(category.value)

    if resources:
        link_list: str = "\n".join(set(resources))

        await interaction.response.send_message(
            embed=create_response(
                f"**{category.name}**\n{link_list}", type="success"
            ),
            ephemeral=True,
            delete_after=60.0,
        )

    else:
        await interaction.response.send_message(
            embed=create_response(
                (
                    f"🇬🇧 No resources found in {category.name}.\n"
                    f"🇫🇷 Aucune ressource trouvée dans {category.name}."
                ),
                type="warning",
            ),
            ephemeral=True,
            delete_after=20.0,
        )


@describe(category="The resource's category")
@choices(category=CATEGORIES)
async def get_resources(
    interaction: Interaction, category: Choice[str] | None = None
) -> None:
    """Display all resources or only those matching category.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).
    category : discord.app_commands.Choice or None, default=None
        If not None, the category to display.

    """
    log_interaction(interaction)

    try:
        if category:
            await get_category_resources(interaction, category)
        else:
            await get_all_resources(interaction)

    except CommandInvokeError as err:
        await interaction.response.send_message(
            embed=create_response("Wrong command.", type="error"),
            ephemeral=True,
            delete_after=20.0,
        )
        programLogger.error(err)

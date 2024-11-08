"""Discord bot client messages formatting."""

from typing import Any, Literal, TypeAlias

from discord import (
    Colour,
    Embed,
    Forbidden,
    HTTPException,
    Interaction,
    InvalidData,
    NotFound,
)

from chatbot.logger import programLogger

LOGS_CHANNEL = None
ResponseType: TypeAlias = Literal["success", "warning", "error"]
TypeToTitle: dict[ResponseType, str] = {
    "success": "✅ SUCCESS",
    "warning": "⚠️ WARNING",
    "error": "❌ ERROR",
}
TypeToColor: dict[ResponseType, int] = {
    "success": 0x2ECC71,
    "warning": 0xF1C40F,
    "error": 0xE74C3C,
}


def set_logs_channel(channel: Any | None) -> None:
    """Set bot logs channel.

    Parameters
    ----------
    channel : Any or None
        The channel object.

    """
    if channel:
        globals()["LOGS_CHANNEL"] = channel


def create_response(message: str, type: ResponseType) -> Embed:
    """Create a command response.

    Parameters
    ----------
    message : str
        The embed content.
    type : ResponseType
        Whether the command failed or not.

    Returns
    -------
    discord.Embed

    """
    embed = Embed(colour=Colour(value=TypeToColor[type]))
    embed.add_field(
        name=TypeToTitle[type],
        value=message,
        inline=False,
    )
    return embed


def log_interaction(interaction: Interaction) -> str:
    """Log command and username for given interaction.

    Parameters
    ----------
    interaction : discord.Interaction
        A user interaction with the bot (slash command).

    Returns
    -------
    str
        The formatted message.

    """
    message: str = (
        f"User '{str(interaction.user.name)}' used command "
        f"'{interaction.command.name}'."
    )
    programLogger.debug(message)

    # NOTE: Return the logged message in case it needs to be used again.
    return message


async def log_bot_action(message: str) -> None:
    """Send message to bot logs channel.

    Parameters
    ----------
    message : str
        The message content as a string.

    Raises
    ------
    RuntimeError
        If the channel can't be fetched or the message can't be sent.

    """
    programLogger.debug(message)

    if not LOGS_CHANNEL:
        programLogger.error("Failed fetching bot logs channel.")
        return

    try:
        await LOGS_CHANNEL.send(message, suppress_embeds=True)

    except (InvalidData, HTTPException, NotFound, Forbidden) as err:
        raise RuntimeError(err)

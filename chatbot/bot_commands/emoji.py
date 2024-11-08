"""Command callbacks for emoji reactions."""

from discord import Forbidden, Guild, Member, RawReactionActionEvent, Role
from discord.ext.commands import Bot

from chatbot.logger import programLogger

from .formatting import log_bot_action

# Emojis reactions the bot must process
EMOJI_REACTIONS: list[str] = ["📌", "🟨", "🟦"]
# Emojis to role IDs
ROLE_IDS: dict[str, int] = {
    "🟨": 1294578631879692350,
    "🟦": 1294579583873449994,
}


async def add_role(client: Bot, payload: RawReactionActionEvent) -> None:
    """Give role when the user reacts with emoji.

    Parameters
    ----------
    client : discord.ext.commands.Bot
        The bot client.
    payload : discord.RawReactionActionEvent
        The reaction event.

    Raises
    ------
    RuntimeError

    """
    action: str = (
        f"User {str(payload.member.name)} added emoji {payload.emoji.name}"
    )
    guild: Guild | None = client.get_guild(payload.guild_id)

    if not guild:
        raise RuntimeError(f"{action}: Guild not found.")

    role: Role | None = guild.get_role(ROLE_IDS[payload.emoji.name])

    if not role:
        raise RuntimeError(f"{action}: Role not found.")

    await payload.member.add_roles(role)
    programLogger.notice(f"{action}: Role given.")


async def remove_role(client: Bot, payload: RawReactionActionEvent) -> None:
    """Remove role when the user removes emoji reaction.

    Parameters
    ----------
    client : discord.ext.commands.Bot
        The bot client.
    payload : discord.RawReactionActionEvent
        The reaction event.

    Raises
    ------
    RuntimeError

    """
    action: str = f"User removed emoji {payload.emoji.name}"
    guild: Guild | None = client.get_guild(payload.guild_id)

    if not guild:
        raise RuntimeError(f"{action}: Guild not found.")

    role: Role | None = guild.get_role(ROLE_IDS[payload.emoji.name])
    member: Member | None = guild.get_member(payload.user_id)

    if not member:
        raise RuntimeError(
            f"{action}: Unexisting user ID '{payload.user_id}'."
        )

    if not role:
        raise RuntimeError(f"{action}: Role not found.")

    action = f"User {member.name} removed emoji {payload.emoji.name}"
    await member.remove_roles(role)
    programLogger.notice(f"{action}: Role removed.")


async def handle_pin_request(
    client: Bot, payload: RawReactionActionEvent, pin: bool
) -> None:
    """Pin or unpin message.

    Parameters
    ----------
    client : discord.ext.commands.Bot
        The bot client.
    payload : discord.RawReactionActionEvent
        The reaction event.
    pin : bool
        Whether the message must be pinned.

    Raises
    ------
    RuntimeError

    """
    action: str = (
        f"User {str(payload.member.name)} wants to pin message"
        if pin
        else f"User {str(payload.user_id)} wants to unpin message"
    )

    try:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if pin:
            await message.pin()
        else:
            await message.unpin()

    except Forbidden as err:
        raise RuntimeError(
            f"{action}: Missing permissions for channel {payload.channel_id}."
        ) from err


async def process_emoji_reaction(
    client: Bot,
    payload: RawReactionActionEvent,
    roles_message_id: int,
    is_added: bool,
) -> None:
    """Process emoji reaction to message.

    Parameters
    ----------
    client : discord.ext.commands.Bot
        The bot client.
    payload : discord.RawReactionActionEvent
        The reaction event.
    roles_message_id : int
        ID of the message to react to to get roles.
    is_added : bool
        True if the emoji was added. Otherwise, it was removed.

    """
    if payload.emoji.name not in EMOJI_REACTIONS:
        return

    try:
        if (
            payload.emoji.name in ROLE_IDS
            and payload.message_id == roles_message_id
        ):
            if is_added:
                await add_role(client, payload)
            else:
                await remove_role(client, payload)

        else:  # Push-pin emoji
            await handle_pin_request(client, payload, is_added)

    except RuntimeError as err:
        await log_bot_action(str(err))

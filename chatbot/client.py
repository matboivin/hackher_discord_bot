"""Discord bot client class."""

from discord import (
    Forbidden,
    HTTPException,
    Intents,
    InvalidData,
    NotFound,
    Object,
    RawReactionActionEvent,
)
from discord.app_commands import Command
from discord.ext.commands import Bot

from chatbot.bot_commands import (
    add_resource,
    get_resources,
    help,
    process_emoji_reaction,
    set_logs_channel,
)
from chatbot.logger import programLogger


async def send_message_to_channel(
    client: Bot, channel_id: int, message: str
) -> None:
    """Send message to a given channel.

    Parameters
    ----------
    client : discord.ext.commands.Bot
        The bot client.
    channel_id : int
        The channel ID.
    message : str
        The message content as a string.

    Raises
    ------
    RuntimeError
        If the channel can't be fetched or the message can't be sent.

    """
    try:
        channel = await client.fetch_channel(channel_id)
        await channel.send(message, suppress_embeds=True)

    except (InvalidData, HTTPException, NotFound, Forbidden) as err:
        raise RuntimeError(err)


def init_bot(prefix: str = "!", intents: Intents = Intents.default()) -> Bot:
    """Initialize the Discord bot.

    Parameters
    ----------
    prefix : str, default='!'
        Prefix the message content must contain to have a command invoked.
    intents : discord.Intents, default=discord.Intents.default()
        Additionnal permissions.

    Returns
    -------
    discord.ext.commands.Bot
        The Discord client.

    """
    # Mandatory to edit user's roles.
    intents.members = True

    return Bot(command_prefix=prefix, intents=intents)


class BotClient:
    """Class defining a Discord bot client.

    Attributes
    ----------
    client : discord.ext.commands.Bot
        The Discord client.
    guild : discord.Object
        The server object.
    roles_message_id : int
        ID of the message to react to to get roles.

    Methods
    -------
    start()
        Run Discord bot.

    """

    def __init__(
        self, bot_token: str, guild_id: int, roles_message_id: int
    ) -> None:
        """Initialize the Discord bot and set parameters.

        Parameters
        ----------
        bot_token : str
            Discord bot token.
        guild_id : int
            The server ID.
        roles_message_id : int
            ID of the message to react to to get roles.

        """
        self.client: Bot = init_bot()
        self.bot_token = bot_token
        self.guild = Object(id=guild_id)
        self.roles_message_id: int = roles_message_id

    def register_guild_callbacks(self, logs_channel_id: int) -> None:
        """Register commands.

        Parameters
        ----------
        logs_channel_id : int
            ID of the bot logs channel.

        """
        # Clear commands
        # for server in client.guilds:
        #     client.tree.clear_commands(guild=Object(id=server.id))

        self.client.tree.add_command(
            Command(
                name="help",
                description="Show available commands.",
                callback=help,
            ),
            guild=self.guild,
        )
        self.client.tree.add_command(
            Command(
                name="add_resource",
                description="Index a resource's link.",
                callback=add_resource,
            ),
            guild=self.guild,
        )
        self.client.tree.add_command(
            Command(
                name="get_resources",
                description="Display resources matching provided category.",
                callback=get_resources,
            ),
            guild=self.guild,
        )

        @self.client.event
        async def on_ready() -> None:
            """Sync the application commands and log when bot is ready."""
            await self.client.tree.sync(guild=self.guild)
            set_logs_channel(self.client.get_channel(logs_channel_id))

            programLogger.notice(f"Bot '{self.client.user}' connected.")

        @self.client.event
        async def on_raw_reaction_add(payload: RawReactionActionEvent) -> None:
            """Give role or pin message when the user reacts with emoji."""
            await process_emoji_reaction(
                self.client, payload, self.roles_message_id, True
            )

        @self.client.event
        async def on_raw_reaction_remove(
            payload: RawReactionActionEvent,
        ) -> None:
            """Remove role or unpin message when the user removes emoji."""
            await process_emoji_reaction(
                self.client, payload, self.roles_message_id, False
            )

    def start(self) -> None:
        """Run Discord bot."""
        self.client.run(self.bot_token)

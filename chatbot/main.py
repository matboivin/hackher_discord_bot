"""Discord bot to index training resources."""

from argparse import ArgumentParser, Namespace
from os import getenv

from aiohttp.client_exceptions import ClientConnectorError

from .client import BotClient
from .database import init_db_connection
from .logger import log_to_file, programLogger, set_logger


def parse_args() -> Namespace:
    """Parse the arguments of the program.

    Returns
    -------
    argparse.Namespace
        Command line arguments of the program.

    """
    parser: ArgumentParser = ArgumentParser(
        description=(
            "Training resources Discord bot. Set BOT_TOKEN and SERVER_ID in "
            ".env."
        )
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="display debug logs"
    )
    parser.add_argument(
        "-f",
        "--database-file",
        type=str,
        metavar="filename.db",
        default="logs/resources.db",
        help="SQLite database filename (default: 'logs/resources.db')",
    )

    return parser.parse_args()


def main() -> None:
    """Program's entrypoint."""
    args: Namespace = parse_args()
    bot_token: str | None = getenv("BOT_TOKEN")
    server_id: str | None = getenv("SERVER_ID")
    roles_message_id: str | None = getenv("ROLES_MESSAGE_ID")
    bot_channel_id: str | None = getenv("BOT_LOGS_CHANNEL_ID")

    set_logger(args.debug)

    if not all([bot_token, server_id, roles_message_id, bot_channel_id]):
        programLogger.error(
            "Missing environment variables. BOT_TOKEN, SERVER_ID, "
            "ROLES_MESSAGE_ID and BOT_LOGS_CHANNEL_ID must be set in .env file."
        )
        return

    try:
        init_db_connection(args.database_file)
        bot = BotClient(
            bot_token,  # type: ignore
            int(server_id),  # type: ignore
            int(roles_message_id),  # type: ignore
        )
        bot.register_guild_callbacks(int(bot_channel_id))  # type: ignore

        bot.start()

    except ClientConnectorError as err:
        log_to_file(err)


if __name__ == "__main__":
    main()

"""Send message to a specific channel using the bot."""

from argparse import ArgumentParser, Namespace
from asyncio import CancelledError, Task, create_task, run
from os import getenv
from pathlib import Path

from aiohttp.client_exceptions import ClientConnectorError
from discord.ext.commands import Bot

from chatbot.client import init_bot, send_message_to_channel
from chatbot.logger import log_to_file, programLogger, set_logger


def parse_args() -> Namespace:
    """Parse the arguments of the program.

    Returns
    -------
    argparse.Namespace
        Command line arguments of the program.

    """
    parser: ArgumentParser = ArgumentParser(
        description="Send message to given channel with Discord bot."
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="display debug logs"
    )
    parser.add_argument(
        "channel_id",
        type=int,
        help="ID of the channel to send the message to",
    )
    parser.add_argument(
        "filepath",
        type=str,
        help=(
            "path to the file that contains the message content (example: "
            "markdown or text)"
        ),
    )

    return parser.parse_args()


async def start_bot_task(args: Namespace, bot_token: str) -> None:
    """Start bot task.

    Parameters
    ----------
    args : argparse.Namespace
        The command-line arguments.
    bot_token : str
        The Discord bot token.

    """
    task: Task[None] | None = None

    try:
        client: Bot = init_bot()
        message: str = Path(args.filepath).read_text()

        @client.event
        async def on_ready() -> None:
            programLogger.notice(f"Bot '{client.user}' connected")

            try:
                await send_message_to_channel(client, args.channel_id, message)
            except RuntimeError as err:
                programLogger.error(err)

            if task:
                task.cancel()

        task = create_task(client.start(bot_token, reconnect=False))
        await task

    except CancelledError:
        pass

    except ClientConnectorError as err:
        log_to_file(err)

    finally:
        await client.close()


def main() -> None:
    """Program's entrypoint."""
    args: Namespace = parse_args()
    bot_token: str | None = getenv("BOT_TOKEN")

    set_logger(args.debug)

    if not bot_token:
        programLogger.error(
            "Missing environment variables. BOT_TOKEN must be set in .env file."
        )
        return

    try:
        run(start_bot_task(args, bot_token))

    except KeyboardInterrupt:
        programLogger.debug("Program interrupted by keyboard.")


if __name__ == "__main__":
    main()

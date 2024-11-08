# HackHer - Discord bot

Discord bot for our CTF team server.

## Table of Content

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
    - [Extra features](#extra-features)
- [Contributing](#contributing)

## Prerequisites

- A Discord bot
- An environment to run the bot (Raspberry Pi, VPS, ...)
- Docker
- Docker Compose v2
- Optional: GNU make (a Makefile is provided for a more friendly use)

## Installation

1. Clone the repository and change it to your working directory.

2. Set the environment variables in a `.env` file:

   ```sh
   COMPOSE_PROJECT_NAME=  # Name of the project
   COMPOSE_FILE=docker-compose.yml
   BOT_TOKEN=  # Token of the Telegram bot
   DATABASE_PATH=  # Path to the SQLite file
   SERVER_ID=  # ID of the Discord server (aka guild ID)
   BOT_LOGS_CHANNEL_ID=  # ID of the channel where to log bot actions
   ROLES_MESSAGE_ID=  # ID of the message to react to to get roles
   ```

3. Build the project:

   ```console
   $ make up-build
   ```

## Usage

```
chatbot [-h] [-d] [-f filename.db]

Training resources Discord bot. Set BOT_TOKEN and SERVER_ID in .env.

options:
  -h, --help            show this help message and exit
  -d, --debug           display debug logs
  -f filename.db, --database-file filename.db
                        SQLite database filename (default: 'logs/resources.db')
```

Update the `command` key in the [Docker Compose file](docker-compose.yml) and pass the arguments you need.

### Extra features

You can send a message thanks to [script `helpers/send_message.py`](helpers/send_message.py):

```
send_message.py [-h] [-d] channel_id filepath

Send message to given channel with Discord bot.

positional arguments:
  channel_id   ID of the channel to send the message to
  filepath     path to the file that contains the message content (example: markdown or text)

options:
  -h, --help   show this help message and exit
  -d, --debug  display debug logs
```

## Contributing

If you want to contribute to the bot's development, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

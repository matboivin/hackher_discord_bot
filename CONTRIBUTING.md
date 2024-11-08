# Contributing

Follow this guide if you want to develop a new feature or modify the bot's code.

## Prerequisites

- A Discord bot
- [Poetry](https://python-poetry.org/)
- Python >=3.10
- Docker
- Docker Compose v2
- Optional: GNU make (a Makefile is provided for a more friendly use)

## Installation

1. Clone the repository and change it to your working directory.

2. Set the environment variables in a `.env` file:

   ```sh
   COMPOSE_PROJECT_NAME=  # Name of the project
   COMPOSE_FILE=docker-compose.yml:docker-compose.dev.yml
   BOT_TOKEN=  # Token of the Telegram bot
   DATABASE_PATH=  # Path to the SQLite file
   SERVER_ID=  # ID of the Discord server (aka guild ID)
   BOT_LOGS_CHANNEL_ID=  # ID of the channel where to log bot actions
   ROLES_MESSAGE_ID=  # ID of the message to react to to get roles
   ```

3. Install the project:

   ```sh
   $ poetry install
   ```

   Optional: If you want to create the virtual environment in a .venv folder inside the project's directory, run:

   ```sh
   $ poetry config virtualenvs.in-project true
   ```

   Activate the Python virtual environment:

   ```sh
   $ poetry shell
   ```

   Install the pre-commit hooks (for formatting and linting) that will run before every commit:

   ```sh
   $ pre-commit install
   ```

4. Write code.

5. Push your changes on a new branch.

6. Open a Merge Request and wait for the maintainers to review your code.

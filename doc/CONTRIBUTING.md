# Contributing

Follow this guide if you want to develop a new feature or modify the bot's code.

## Prerequisites

- A Discord bot
- Docker
- Docker Compose v2
- Optional: GNU make (a Makefile is provided for a more friendly use)

## Installation

1. Clone the repository and change it to your working directory.

2. Set the environment variables in a `.env` file:

   ```sh
   TIMEZONE=
   COMPOSE_PROJECT_NAME=  # Name of the project
   COMPOSE_FILE=docker-compose.yml:docker-compose.dev.yml  # Important to append the development Docker Compose file
   BOT_TOKEN=  # Token of the Discord bot
   DATABASE_PATH=  # Path to the SQLite file
   SERVER_ID=  # ID of the Discord server (aka guild ID)
   BOT_LOGS_CHANNEL_ID=  # ID of the channel where to log bot actions
   ROLES_MESSAGE_ID=  # ID of the message to react to to get roles
   ```

3. Build the project:

   ```console
   $ make up-build
   ```

4. Enter the container:

   ```sh
   $ docker exec -ti <container_name> sh
   ```

   Activate the Python virtual environment:

   ```sh
   $ source .venv/bin/activate
   ```

   Install the pre-commit hooks (for formatting and linting) that will run before every commit:

   ```sh
   $ pre-commit install
   ```

5. Write code. The source files are mounted as volumes and will be updated on your host.

6. Push your changes on a new branch.

7. Open a Merge Request and wait for the maintainers to review your code.

import os
import sys

from dotenv import load_dotenv
load_dotenv()


def get_token():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("No token found. Add entry BOT_TOKEN to .env file to get started")
        sys.exit(1)
    return token


def main():
    from wootbot import WootBot
    bot = WootBot.create_instance()
    bot.run(get_token())


if __name__ == "__main__":
    main()
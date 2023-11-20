# WOOT Bot
This is a bot for summarizing mini games posted in a discord channel. Right now it supports
* Wordle
* Ordel
* Ordlig
* Tradle

## Key idea
Every day at midnight the bot collects all posts since yesterday in a certain channel and looks for headers that indicate point reports. It will then combine these results into an ascii table and post to the same discord channel.

## How to get started
1. Create a bot on discord
2. Add your bot to your server with privileges to read and write messages
3. Clone this repo
4. Create a file called .env in the root folder
5. Copy your token for the bot into the .env file as `BOT_TOKEN=YOUR_TOKEN`
6. Create a virtual env with `python -m venv .venv` and activate it
7. Install dependencies with `pip install -r requirements.txt`
8. Run main.py

## Upcoming features (?)
* Parse results in plain text
* Handle names in some smart way to make sure table isn't too wide on smartphones
* Being able to set what channel it listens to. Right now it is hardcoded to 'daily-highscores'.
* More?
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
3. Copy your token for the bot and paste into the .env file
4. Run main.py
5. Be happy!

## Upcoming features (?)
* Parse results in plain text
* Handle names in some smart way to make sure table isn't too wide on smartphones
* Being able to set what channel it listens to. Right now it is hardcoded to 'daily-highscores'.
* More?